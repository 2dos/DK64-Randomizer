"""Server code for the randomizer."""

import codecs
import json
from os import path, walk, environ, makedirs, listdir, remove
import random
import time
import traceback
import zipfile
from io import BytesIO
from multiprocessing import Process, Queue
from queue import Empty

from flask import Flask, make_response, request, send_from_directory
from flask_cors import CORS
from flask_executor import Executor
from vidua import bps

from randomizer.Enums.Settings import SettingsMap
from randomizer.Fill import Generate_Spoiler
from randomizer.Patching.Patcher import load_base_rom
from randomizer.Settings import Settings
from randomizer.SettingStrings import encrypt_settings_string_enum, decrypt_settings_string_enum
from randomizer.Spoiler import Spoiler
from git import Repo
from datetime import datetime as Datetime
from datetime import UTC
from apscheduler.schedulers.background import BackgroundScheduler
from version import version

local_repo = Repo(path="./")
local_branch = local_repo.active_branch.name

if __name__ == "__main__":
    app = Flask(__name__, static_url_path="", static_folder="")
else:
    app = Flask(__name__)
app.config["EXECUTOR_MAX_WORKERS"] = environ.get("EXECUTOR_MAX_WORKERS", 2)
app.config["EXECUTOR_TYPE"] = environ.get("EXECUTOR_TYPE", "process")
executor = Executor(app)
CORS(app)
current_total = 0
try:
    with open("current_total.cfg", "r") as f:
        current_total = int(f.read())
except Exception:
    # If we can't read the file, just set it to 0 in the file.
    with open("current_total.cfg", "w") as f:
        f.write("0")
last_generated_time = Datetime.now(UTC)
try:
    with open("last_generated_time.cfg", "r") as f:
        last_generated_time = Datetime.strptime(f.read(), "%Y-%m-%d %H:%M:%S.%f")
except Exception:
    # If we can't read the file, just set it to 0 in the file.
    with open("last_generated_time.cfg", "w") as f:
        f.write(str(last_generated_time))
TIMEOUT = environ.get("TIMEOUT", 400)
patch = open("./static/patches/shrink-dk64.bps", "rb")
original = open("dk64.z64", "rb")
# load all the settings strings into memory
og_patched_rom = None
presets = []
with open("static/presets/preset_files.json", "r") as f:
    presets = json.load(f)
# Check if we have a file named local_presets.json and load it
if path.isfile("local_presets.json"):
    with open("local_presets.json", "r") as f:
        local_presets = json.load(f)
        for local_preset in local_presets:
            # Look for a preset with the same name
            found_preset = False
            for i, global_preset in enumerate(presets):
                if global_preset.get("name") == local_preset.get("name"):
                    # Update the global preset with the local preset
                    presets[i] = local_preset
                    found_preset = True
                    break
            # If not found, append the local preset
            if not found_preset:
                presets.append(local_preset)


if environ.get("HOSTED_SERVER") is not None:
    import boto3

    dynamodb = boto3.resource("dynamodb", region_name="us-west-2")


def generate(default_rom, generate_settings, queue, post_body):
    """Gen a seed and write the file to an output file."""
    try:
        load_base_rom(default_file=default_rom)
        settings = Settings(generate_settings)
        spoiler = Spoiler(settings)
        patch, spoiler = Generate_Spoiler(spoiler)
        spoiler.FlushAllExcessSpoilerData()
        return_dict = {}
        return_dict["patch"] = patch
        return_dict["spoiler"] = spoiler
        queue.put(return_dict)

    except Exception as e:
        if environ.get("HOSTED_SERVER") is not None:
            write_error(traceback.format_exc(), post_body)
        print(traceback.format_exc())
        # Return the error and the type of error.
        error = str(type(e).__name__) + ": " + str(e)
        queue.put(error)


def start_gen(gen_key, post_body):
    """Start the generation process."""
    print("starting generation")
    setting_data = post_body
    global og_patched_rom
    if og_patched_rom is None:
        global original
        global patch
        og_patched_rom = BytesIO(bps.patch(original, patch).read())
    if not setting_data.get("seed"):
        setting_data["seed"] = random.randint(0, 100000000)
    # Convert string data to enums where possible.
    for k, v in setting_data.items():
        if k in SettingsMap:
            if type(v) is list:
                values = []
                for val in v:
                    if type(val) is int:
                        values.append(SettingsMap[k](val))
                    else:
                        values.append(SettingsMap[k][val])
                setting_data[k] = values
            elif type(v) is int:
                setting_data[k] = SettingsMap[k](v)
            else:
                try:
                    setting_data[k] = SettingsMap[k][v]
                except Exception:
                    pass
    try:
        queue = Queue()
        p = Process(
            target=generate,
            args=(
                og_patched_rom,
                setting_data,
                queue,
                post_body,
            ),
        )
        p.start()
        try:
            return_data = queue.get(timeout=TIMEOUT)
        # raise an exception if we timeout
        except Empty:
            try:
                p.kill()
            except Exception:
                pass
            return "Seed Generation Timed Out"
        p.join(0)
        if type(return_data) is str:
            return return_data
        else:
            # Assuming post_body.get("delayed_spoilerlog_release") is an int, and its the number of hours to delay the spoiler log release convert that to time.time() + hours as seconds.
            try:
                spoiler_log_release = int(post_body.get("delayed_spoilerlog_release", 0))
            except ValueError:
                spoiler_log_release = 0

            if spoiler_log_release == 0:
                # Lets set it to 5 years from now if we don't have a delayed spoiler log release, it'll be deleted after 4 weeks anyway.
                unlock_time = time.time() + 157784760
            else:
                unlock_time = time.time() + (spoiler_log_release * 3600)
            if setting_data.get("generate_spoilerlog", True):
                unlock_time = 0

            # Append the current time to the spoiler log as unlock_time.
            patch = return_data["patch"]
            spoiler = return_data["spoiler"]
            return patch, spoiler, unlock_time, time.time()

    except Exception as e:
        if environ.get("HOSTED_SERVER") is not None:
            write_error(traceback.format_exc(), post_body)
        print(traceback.format_exc())
        error = str(type(e).__name__) + ": " + str(e)
        return error


def write_error(error, settings_string):
    """Write an error to the error table."""
    try:
        converted_settings_string = encrypt_settings_string_enum(settings_string)
    except Exception:
        converted_settings_string = "Settings String failed to convert"
    error_table = dynamodb.Table("dk64_error_db")
    error_table.put_item(
        Item={"time": str(time.time()), "error_data": str(error), "settings": str(converted_settings_string), "branch": local_branch, "plando": str(settings_string.get("enable_plandomizer", False))}
    )


@app.route("/generate", methods=["GET", "POST"])
def lambda_function():
    """Lambda function to generate a seed.

    Returns:
        Response: Flask response object.
    """
    # Check if the request is an OPTIONS request if so drop it.
    if request.method == "OPTIONS":
        return make_response("", 200)
    # Flask get the query string parameters as a dict.
    query_string = request.args.to_dict()
    # See if we have a query for gen_key.
    if query_string.get("gen_key"):
        gen_key = str(query_string.get("gen_key"))
        if executor.futures._futures.get(gen_key) and not executor.futures.done(gen_key):
            # We're not done generating yet
            # Create an ordered dict of the existing future that are not done.
            ordered_futures = {}
            for key in executor.futures._futures:
                if not executor.futures.done(key) and not executor.futures.running(key):
                    ordered_futures[key] = executor.futures._futures[key]
            try:
                job_index = list(ordered_futures).index(gen_key)
                if job_index < 0:
                    job_index = 0
            except Exception as e:
                job_index = 0
            response = make_response(json.dumps({"status": executor.futures._state(gen_key), "position": job_index}), 202)
            response.mimetype = "application/json"
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
        elif executor.futures._futures.get(gen_key):
            # We're done generating, return the data.
            future = executor.futures.pop(gen_key)
            resp_data = future.result()
            if type(resp_data) is str:
                response = make_response(resp_data, 208)
                return response
            hash = resp_data[1].settings.seed_hash
            spoiler_log = json.loads(resp_data[1].json)
            unlock_time = resp_data[2]
            spoiler_log["Unlock Time"] = unlock_time
            generated_time = resp_data[3]
            spoiler_log["Generated Time"] = generated_time
            current_seed_number = update_total()
            file_name = str(current_seed_number)
            # write the spoiler log to a file in generated_seeds folder. Create the folder if it doesn't exist.
            makedirs("generated_seeds", exist_ok=True)
            with open("generated_seeds/" + file_name + ".json", "w") as f:
                f.write(str(json.dumps(spoiler_log)))

            sections_to_retain = ["Settings", "Cosmetics", "Spoiler Hints", "Spoiler Hints Data", "Generated Time"]
            if resp_data[1].settings.generate_spoilerlog is False:
                spoiler_log = {k: v for k, v in spoiler_log.items() if k in sections_to_retain}
            else:
                del spoiler_log["Unlock Time"]

            patch = resp_data[0]
            # Zip all the data into a single file.
            # Create a new zip file
            zip_data = BytesIO()

            with zipfile.ZipFile(zip_data, "w") as zip_file:
                # Write each variable to the zip file
                zip_file.writestr("patch", patch)
                zip_file.writestr("hash", str(hash))
                zip_file.writestr("spoiler_log", str(json.dumps(spoiler_log)))
                zip_file.writestr("seed_id", str(resp_data[1].settings.seed_id))
                zip_file.writestr("generated_time", str(generated_time))
                zip_file.writestr("version", version)
                zip_file.writestr("seed_number", str(current_seed_number))
            zip_data.seek(0)
            # Convert the zip to a string of base64 data
            zip_conv = codecs.encode(zip_data.getvalue(), "base64").decode()
            # Store the patch file in generated_seeds folder.
            makedirs("generated_seeds", exist_ok=True)
            with open("generated_seeds/" + file_name + ".lanky", "w") as f:
                f.write(zip_conv)
            # Return it as a text file
            response = make_response(zip_conv, 200)
            return response
        else:
            # We don't have a future for this key, so we need to start generating.
            print("Starting generation from webworker: " + str(gen_key))
            post_body = json.loads(request.get_json().get("post_body"))
            executor.submit_stored(gen_key, start_gen, gen_key, post_body)
            response = make_response(json.dumps({"start_time": gen_key}), 201)
            response.mimetype = "application/json"
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
    else:
        response = make_response(json.dumps({"error": "error"}), 205)
        response.mimetype = "application/json"
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


@app.route("/current_total", methods=["GET"])
def get_current_total():
    """Get the current total seeds generated."""
    response = make_response(json.dumps({"total_seeds": current_total, "last_generated_time": last_generated_time.strftime("%Y-%m-%d %H:%M:%S.%f")}), 200)
    response.mimetype = "application/json"
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


# Create a route for get_spoiler_log that takes a hash as a parameter.
@app.route("/get_spoiler_log", methods=["GET"])
def get_spoiler_log():
    """Get the spoiler log for a seed."""
    # Get the hash from the query string.
    hash = request.args.get("hash")
    # check if hash contains special characters not in an approved list.
    if all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_=" for c in hash):
        file_name = hash
    else:
        return make_response(json.dumps({"error": "error"}), 205)
    fullpath = path.normpath(path.join("generated_seeds/", file_name + ".json"))
    if not fullpath.startswith("generated_seeds/"):
        raise Exception("not allowed")
    # Check if the file exists
    if path.isfile(fullpath):
        # Return the spoiler log
        with open(fullpath, "r") as f:
            current_time = time.time()
            # if the unlock time is less than the current time, return the spoiler log
            file_contents = json.load(f)
            if file_contents.get("Unlock Time", 0) < current_time:
                return make_response(file_contents, 200)
            else:
                # Return an error
                return make_response(json.dumps({"error": "error"}), 425)
    else:
        # Return an error
        return make_response(json.dumps({"error": "error"}), 205)


# get the current version of the randomizer
@app.route("/get_version", methods=["GET"])
def get_version():
    """Get the current version of the randomizer."""
    response = make_response(json.dumps({"version": version}), 200)
    response.mimetype = "application/json"
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


# return the preset files for the randomizer
@app.route("/get_presets", methods=["GET"])
def get_presets():
    """Get the preset files for the randomizer."""
    # If the parameter return_blank is not set to true, check if any of the descriptions lengths are less than 3, if so don't include that preset.
    return_blank = request.args.get("return_blank")
    presets_to_return = []
    if return_blank is None:
        for preset in presets:
            if preset.get("settings_string") is None:
                continue
            else:
                presets_to_return.append(preset)
    else:
        # Return all presets that have a settings_string, the first entry does not have one but we want to return it anyway.
        preset_added = False
        for preset in presets:
            if preset.get("settings_string") is None and not preset_added:
                presets_to_return.append(preset)
                preset_added = True
            elif preset.get("settings_string") is None:
                continue
            else:
                presets_to_return.append(preset)

    response = make_response(json.dumps(presets_to_return), 200)
    response.mimetype = "application/json"
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


def delete_old_files():
    """Delete files that are older than 4 weeks."""
    folder_path = "generated_seeds"
    current_time = time.time()
    makedirs("generated_seeds", exist_ok=True)
    for filename in listdir(folder_path):
        if filename.endswith(".json"):
            file_path = path.join(folder_path, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                generated_time = data.get("Generated Time", 0)

                # Check if it's been 4 weeks since unlock_time
                if current_time - generated_time >= 2419200:  # 4 weeks in seconds
                    remove(file_path)
                    print(f"Deleted file: {filename}")
                    # also delete the lanky file
                    remove(path.join(folder_path, filename.replace(".json", ".lanky")))


@app.route("/get_seed", methods=["GET"])
def get_seed():
    """Get the lanky for a seed."""
    # Get the hash from the query string.
    hash = request.args.get("hash")
    # check if hash contains special characters not in an approved list.
    if all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_=" for c in hash):
        file_name = hash
    else:
        return make_response(json.dumps({"error": "error"}), 205)
    fullpath = path.normpath(path.join("generated_seeds/", str(file_name) + ".json"))
    if not fullpath.startswith("generated_seeds/"):
        raise Exception("not allowed")
    # Check if the file exists
    if path.isfile(fullpath):
        # Return the spoiler log
        with open(fullpath, "r") as f:
            # Get the actual lanky file modify the fullpath to be the lanky file, so we're only changing the file ending for security.
            # Remove the last 5 characters from the fullpath and replace them with .lanky
            fullpath = fullpath[:-5] + ".lanky"
            # Check if the file exists
            if not path.isfile(fullpath):
                # Return an error
                return make_response(json.dumps({"error": "error"}), 205)
            with open(fullpath, "r") as lanky_file:
                # Return the lanky file
                zip_conv = lanky_file.read()
                return make_response(zip_conv, 200)

    else:
        # Return an error
        return make_response(json.dumps({"error": "error"}), 205)


@app.route("/status", methods=["GET"])
def get_status():
    """Lambda function to generate a seed.

    Returns:
        Response: Flask response object.
    """
    # Flask get the query string parameters as a dict.
    query_string = request.args.to_dict()
    # See if we have a query for gen_key.
    if query_string.get("gen_key"):
        gen_key = str(query_string.get("gen_key"))
        if executor.futures._futures.get(gen_key) and not executor.futures.done(gen_key):
            # We're not done generating yet
            # Create an ordered dict of the existing future that are not done.
            ordered_futures = {}
            for key in executor.futures._futures:
                if not executor.futures.done(key) and not executor.futures.running(key):
                    ordered_futures[key] = executor.futures._futures[key]
            try:
                job_index = list(ordered_futures).index(gen_key)
                if job_index < 0:
                    job_index = 0
            except Exception as e:
                job_index = 0
            response = make_response(json.dumps({"status": executor.futures._state(gen_key), "position": job_index}), 200)
            response.mimetype = "application/json"
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
        elif executor.futures._futures.get(gen_key):
            future = executor.futures._futures.get(gen_key)
            resp_data = future.result()
            if type(resp_data) is str:
                response = make_response(json.dumps({"status": "failure", "data": resp_data}), 200)
            else:
                response = make_response(json.dumps({"status": "ready"}), 200)
            response.mimetype = "application/json"
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
        else:
            response = make_response(json.dumps({"status": "stopped"}), 200)
            response.mimetype = "application/json"
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
    else:
        response = make_response(json.dumps({"status": "error"}), 200)
        response.mimetype = "application/json"
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


@app.route("/get_seed_data", methods=["GET"])
def get_seed_data():
    """Lambda function to get a hash of a seed.

    Returns:
        Response: Flask response object.
    """
    # Flask get the query string parameters as a dict.
    query_string = request.args.to_dict()
    # See if we have a query for gen_key.
    if query_string.get("gen_key"):
        gen_key = str(query_string.get("gen_key"))
        if executor.futures._futures.get(gen_key):
            future = executor.futures.pop(gen_key)
            resp_data = future.result()
            if type(resp_data) is str:
                response = make_response(json.dumps({"status": "failure", "data": resp_data}), 200)
                response.mimetype = "application/json"
                response.headers["Content-Type"] = "application/json; charset=utf-8"
                return response
            hash = resp_data[1].settings.seed_hash
            spoiler_log = json.loads(resp_data[1].json)
            # Encrypt the time and hash with the encryption key.
            current_seed_number = update_total()
            file_name = str(current_seed_number)
            unlock_time = resp_data[2]
            generated_time = resp_data[3]
            spoiler_log["Unlock Time"] = unlock_time
            spoiler_log["Generated Time"] = generated_time
            # write the spoiler log to a file in generated_seeds folder. Create the folder if it doesn't exist.
            makedirs("generated_seeds", exist_ok=True)
            with open("generated_seeds/" + file_name + ".json", "w") as f:
                f.write(str(json.dumps(spoiler_log)))

            sections_to_retain = ["Settings", "Cosmetics", "Spoiler Hints", "Spoiler Hints Data", "Generated Time"]
            if resp_data[1].settings.generate_spoilerlog is False:
                spoiler_log = {k: v for k, v in spoiler_log.items() if k in sections_to_retain}
            else:
                del spoiler_log["Unlock Time"]

            patch = resp_data[0]
            # Zip all the data into a single file.
            # Create a new zip file
            zip_data = BytesIO()

            with zipfile.ZipFile(zip_data, "w") as zip_file:
                # Write each variable to the zip file
                zip_file.writestr("patch", patch)
                zip_file.writestr("hash", str(hash))
                zip_file.writestr("spoiler_log", str(json.dumps(spoiler_log)))
                zip_file.writestr("seed_id", str(resp_data[1].settings.seed_id))
                zip_file.writestr("generated_time", str(generated_time))
                zip_file.writestr("version", version)
                zip_file.writestr("seed_number", str(current_seed_number))
            zip_data.seek(0)
            # Convert the zip to a string of base64 data
            zip_conv = codecs.encode(zip_data.getvalue(), "base64").decode()
            # Store the patch file in generated_seeds folder.
            makedirs("generated_seeds", exist_ok=True)
            with open("generated_seeds/" + file_name + ".lanky", "w") as f:
                f.write(zip_conv)
            response = make_response(json.dumps({"status": "complete", "hash": hash, "seed_number": current_seed_number}), 200)
            response.mimetype = "application/json"
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
        else:
            response = make_response(json.dumps({"status": "stopped"}), 200)
            response.mimetype = "application/json"
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
    else:
        response = make_response(json.dumps({"status": "error"}), 200)
        response.mimetype = "application/json"
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


@app.route("/convert_settings_string", methods=["POST"])
def convert_settings_string():
    """Convert a settings string to a post body json."""
    # Get the settings string from the request body
    settings_string = request.get_json().get("settings_string")
    decrypted = decrypt_settings_string_enum(settings_string)
    # Return the json
    return make_response(json.dumps(decrypted), 200)


def update_total():
    """Update the total seeds generated."""
    global current_total
    max_retries = 5  # Maximum number of retries
    retry_delay = random.uniform(0, 3)
    for _ in range(max_retries):
        try:
            # Try to read and update the current total
            with open("current_total.cfg", "r+") as f:
                try:
                    current_total = int(f.read())
                except ValueError:
                    # If the file is empty or has invalid content
                    current_total = 0

                current_total += 1
                f.seek(0)  # Move the file pointer to the beginning
                f.write(str(current_total))
                f.truncate()  # Truncate the file to the current length
                break
        except IOError:
            # If a read/write error occurs, wait for a random delay and retry
            time.sleep(retry_delay)

    # Update last_generated_time
    global last_generated_time
    last_generated_time = Datetime.now(UTC)
    with open("last_generated_time.cfg", "w") as f:
        f.write(str(last_generated_time))
    return current_total


# Setup the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_old_files, trigger="interval", hours=2)
scheduler.start()

if __name__ == "__main__":

    @app.route("/")
    def index():
        """Serve the index page."""
        return send_from_directory(".", "index.html")

    @app.route("/randomizer")
    def rando():
        """Serve the randomizer page."""
        return send_from_directory(".", "randomizer.html")

    extra_dirs = ["./static", "./templates"]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

    app.run(debug=True, port=8000, threaded=True, extra_files=extra_files)
