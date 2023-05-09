from flask import Flask, make_response
import argparse
import codecs
import json
import pickle
import random
import time
from flask_executor import Executor
import traceback

from randomizer.Enums.Settings import SettingsMap
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Spoiler import Spoiler
from flask import request
app = Flask(__name__)
app.config['EXECUTOR_MAX_WORKERS'] = 1
executor = Executor(app)

def generate(generate_settings, file_name, gen_spoiler):
    """Gen a seed and write the file to an output file."""
    settings = Settings(generate_settings)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    return spoiler


def start_gen():
    print("starting generation")
    start = time.time()
    presets = json.load(open("static/presets/preset_files.json"))
    default = json.load(open("static/presets/default.json"))
    found = False
    for file in presets.get("progression"):
        with open("static/presets/" + file, "r") as preset_file:
            data = json.load(preset_file)
            if "Season 1 Race Settings" == data.get("name"):
                setting_data = default
                for key in data:
                    setting_data[key] = data[key]
                setting_data.pop("name")
                setting_data.pop("description")
                found = True
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
        spoiler = generate(setting_data, 'test', True)
    except Exception as e:
        print(traceback.format_exc())
    end = time.time()
    return spoiler.json

@app.route('/start_generation')
def lambda_function():
    """CLI Entrypoint for generating seeds."""
    # Flask get the query string parameters as a dict.
    query_string = request.args.to_dict()
    # See if we have a query for gen_key.
    if query_string.get("gen_key"):
        gen_key = str(query_string.get("gen_key"))
        if executor.futures._futures.get(gen_key) and not executor.futures.done(gen_key):
            return make_response(json.dumps({'status': executor.futures._state(gen_key)}), 200)
        elif executor.futures._futures.get(gen_key):
            future = executor.futures.pop(gen_key)
            return make_response(json.dumps({'status': future.result()}), 200)
        else:
            executor.submit_stored(gen_key, start_gen)
            #response = make_response(json.dumps(spoiler.json), 200)
            response = make_response(json.dumps({"start_time": gen_key}), 200)
            response.mimetype = "text/plain"
            return response
    # Get the current time in milliseconds so we can use it as a key for the future.
    # And a random number to use as a modifier for the key so we don't have to worry about collisions.
    else:
        random_seed = random.randint(0, 100000000)
        start_time = str(int(round(time.time() * 1000)) + random_seed)
        executor.submit_stored(start_time, start_gen)
        #response = make_response(json.dumps(spoiler.json), 200)
        response = make_response(json.dumps({"start_time": start_time}), 200)
        response.mimetype = "text/plain"
        return response
