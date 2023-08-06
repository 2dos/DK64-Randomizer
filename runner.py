"""Server code for the randomizer."""
import codecs
import json
import os
import random
import time
import traceback
import zipfile
from io import BytesIO
from randomizer.Fill import Generate_Spoiler
from randomizer.Patching.Patcher import load_base_rom
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler
from flask import Flask, make_response, request
from randomizer.SettingStrings import encrypt_settings_string_enum

from flask_cors import CORS
from flask_executor import Executor
from multiprocessing import Process, Queue
from randomizer.Enums.Settings import SettingsMap
from queue import Empty
from vidua import bps


app = Flask(__name__)
app.config["EXECUTOR_MAX_WORKERS"] = os.environ.get("EXECUTOR_MAX_WORKERS", 2)
app.config["EXECUTOR_TYPE"] = os.environ.get("EXECUTOR_TYPE", "process")
executor = Executor(app)
CORS(app)
TIMEOUT = 300
current_job = []

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
        print("Returning")
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
    global current_job
    if current_job is None:
        current_job = []
    current_job.append(gen_key)
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
            current_job.remove(gen_key)
            return patch, spoiler

    except Exception as e:
        if os.environ.get("HOSTED_SERVER") is not None:
            write_error(traceback.format_exc(), post_body)
        current_job.remove(gen_key)
        print(traceback.format_exc())
        error = str(type(e).__name__) + ": " + str(e)
        return error


def write_error(error, settings_string):
    """Write an error to the error table."""
    converted_settings_string = encrypt_settings_string_enum(settings_string)
    error_table = dynamodb.Table("dk64_error_db")
    error_table.put_item(
        Item={
            "time": str(time.time()),
            "error_data": str(error),
            "settings": str(converted_settings_string),
        }
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
            global current_job
            if str(gen_key) in current_job:
                response = make_response(json.dumps({"status": executor.futures._state(gen_key)}), 203)
            else:
                response = make_response(json.dumps({"status": executor.futures._state(gen_key)}), 202)
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
            if os.environ.get("HOSTED_SERVER") is not None:
                seed_table = dynamodb.Table("seed_db")
                seed_table.put_item(
                    Item={
                        "time": str(time.time()) + str(hash),
                        "seed_id": str(resp_data[1].settings.seed_id),
                        "spoiler_log": str(json.dumps(spoiler_log)),
                    }
                )
            sections_to_retain = ["Settings", "Cosmetics"]
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
            zip_data.seek(0)

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
