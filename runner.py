"""Server code for the randomizer."""
import codecs
import json
import os
import random
import time
import traceback
from file_encryption import random_string, encrypt_string
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
from randomizer.SettingStrings import encrypt_settings_string_enum
from randomizer.Spoiler import Spoiler
from git import Repo
from datetime import datetime as Datetime
from apscheduler.schedulers.background import BackgroundScheduler
from version import version

local_repo = Repo(path="./")
local_branch = local_repo.active_branch.name

if __name__ == "__main__":
    app = Flask(__name__, static_url_path="", static_folder="")
else:
    app = Flask(__name__)
app.config["EXECUTOR_MAX_WORKERS"] = os.environ.get("EXECUTOR_MAX_WORKERS", 2)
app.config["EXECUTOR_TYPE"] = os.environ.get("EXECUTOR_TYPE", "process")
executor = Executor(app)
CORS(app, resources={"*": {"origins": ["dk64randomizer.com", "dev.dk64randomizer.com", "localhost:8000"]}})
current_total = 0
try:
    with open("current_total.cfg", "r") as f:
        current_total = int(f.read())
except Exception:
    # If we can't read the file, just set it to 0 in the file.
    with open("current_total.cfg", "w") as f:
        f.write("0")
last_generated_time = Datetime.utcnow()
try:
    with open("last_generated_time.cfg", "r") as f:
        last_generated_time = Datetime.strptime(f.read(), "%Y-%m-%d %H:%M:%S.%f")
except Exception:
    # If we can't read the file, just set it to 0 in the file.
    with open("last_generated_time.cfg", "w") as f:
        f.write(str(last_generated_time))
TIMEOUT = os.environ.get("TIMEOUT", 400)
Encryption_Key = os.environ.get("ENCRYPTION_KEY", random_string(128))
patch = open("./static/patches/shrink-dk64.bps", "rb")
original = open("dk64.z64", "rb")
og_patched_rom = BytesIO(bps.patch(original, patch).read())

if os.environ.get("HOSTED_SERVER") is not None:
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
        if os.environ.get("HOSTED_SERVER") is not None:
            write_error(traceback.format_exc(), post_body)
        print(traceback.format_exc())
        # Return the error and the type of error.
        error = str(type(e).__name__) + ": " + str(e)
        queue.put(error)


def start_gen(gen_key, post_body):
    """Start the generation process."""
    print("starting generation")
    setting_data = post_body
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
            patch = return_data["patch"]
            spoiler = return_data["spoiler"]
            return patch, spoiler

    except Exception as e:
        if os.environ.get("HOSTED_SERVER") is not None:
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
            # Only retain the Settings section and the Cosmetics section.
            unlock_time = None
            generated_time = time.time()
            if os.environ.get("HOSTED_SERVER") is not None:
                try:
                    seed_table = dynamodb.Table("seed_db")
                    seed_table.put_item(
                        Item={
                            "time": str(time.time()) + str(hash),
                            "seed_id": str(resp_data[1].settings.seed_id),
                            "spoiler_log": str(json.dumps(spoiler_log)),
                        }
                    )
                except Exception:
                    pass
                # Encrypt the time and hash with the encryption key.
                file_name = encrypt_string(str(str(hash) + str(resp_data[1].settings.seed_id)), Encryption_Key)
                # Get the current time and add 5 hours to it.
                unlock_time = time.time() + 18000
                # Append the current time to the spoiler log as unlock_time.
                spoiler_log["Unlock_Time"] = unlock_time
                spoiler_log["Generated_Time"] = generated_time
                # write the spoiler log to a file in generated_seeds folder. Create the folder if it doesn't exist.
                os.makedirs("generated_seeds", exist_ok=True)
                with open("generated_seeds/" + file_name + ".json", "w") as f:
                    f.write(str(json.dumps(spoiler_log)))

            sections_to_retain = ["Settings", "Cosmetics", "Spoiler Hints", "Spoiler Hints Data", "Generated_Time", "Unlock_Time"]
            if resp_data[1].settings.generate_spoilerlog is False:
                spoiler_log = {k: v for k, v in spoiler_log.items() if k in sections_to_retain}

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
                if unlock_time is not None:
                    zip_file.writestr("file_string", str(file_name))
            zip_data.seek(0)
            update_total()
            # Convert the zip to a string of base64 data
            zip_conv = codecs.encode(zip_data.getvalue(), "base64").decode()
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
    fullpath = os.path.normpath(os.path.join("generated_seeds/", file_name + ".json"))
    if not fullpath.startswith("generated_seeds/"):
        raise Exception("not allowed")
    # Check if the file exists
    if os.path.isfile(fullpath):
        # Return the spoiler log
        with open(fullpath, "r") as f:
            current_time = time.time()
            # if the unlock time is less than the current time, return the spoiler log
            file_contents = json.load(f)
            if file_contents.get("Unlock_Time", 0) < current_time:
                return make_response(file_contents, 200)
            else:
                # Return an error
                return make_response(json.dumps({"error": "error"}), 425)
    else:
        # Return an error
        return make_response(json.dumps({"error": "error"}), 205)


def delete_old_files():
    """Delete files that are older than 7 days."""
    folder_path = "generated_seeds"
    current_time = time.time()
    os.makedirs("generated_seeds", exist_ok=True)
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                unlock_time = data.get("Unlock_Time", 0)

                # Check if it's been seven days since unlock_time
                if current_time - unlock_time >= 604800:  # 7 days in seconds
                    os.remove(file_path)
                    print(f"Deleted file: {filename}")


def update_total():
    """Update the total seeds generated."""
    global current_total
    current_total += 1
    with open("current_total.cfg", "w") as f:
        f.write(str(current_total))
    global last_generated_time
    last_generated_time = Datetime.utcnow()
    with open("last_generated_time.cfg", "w") as f:
        f.write(str(last_generated_time))


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

    app.run(debug=True, port=8000)
