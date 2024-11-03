"""CLI script for running seed generation."""

import argparse
import codecs
import json
import os
import random
import sys
import time
import traceback
import zipfile
from io import BytesIO

import boto3

from randomizer.Enums.Settings import SettingsMap
from randomizer.Fill import Generate_Spoiler
from randomizer.Patching.Patcher import load_base_rom
from randomizer.Settings import Settings
from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Spoiler import Spoiler

load_base_rom()
dynamodb = boto3.resource("dynamodb", aws_access_key_id=os.environ.get("AWS_ID"), aws_secret_access_key=os.environ.get("AWS_KEY"), region_name="us-west-2")


def generate(generate_settings, file_name):
    """Gen a seed and write the file to an output file."""
    settings = Settings(generate_settings)
    spoiler = Spoiler(settings)
    patch, spoiler = Generate_Spoiler(spoiler)
    hash = spoiler.settings.seed_hash
    spoiler_log = json.loads(spoiler.json)
    # Only retain the Settings section and the Cosmetics section.
    if os.environ.get("HOSTED_SERVER") is not None:
        seed_table = dynamodb.Table("seed_db")
        seed_table.put_item(
            Item={
                "time": str(time.time()) + str(hash),
                "seed_id": str(spoiler.settings.seed_id),
                "spoiler_log": str(json.dumps(spoiler_log)),
            }
        )
    sections_to_retain = ["Settings", "Cosmetics", "Spoiler Hints", "Spoiler Hints Human Readable", "Item Pool"]
    if spoiler.settings.generate_spoilerlog is False:
        spoiler_log = {k: v for k, v in spoiler_log.items() if k in sections_to_retain}

    # Zip all the data into a single file.
    # Create a new zip file
    zip_data = BytesIO()
    with zipfile.ZipFile(zip_data, "w") as zip_file:
        # Write each variable to the zip file
        zip_file.writestr("patch", patch)
        zip_file.writestr("hash", str(hash))
        zip_file.writestr("spoiler_log", str(json.dumps(spoiler_log)))
        zip_file.writestr("seed_id", str(spoiler.settings.seed_id))
    zip_data.seek(0)

    # Convert the zip to a string of base64 data
    zip_conv = codecs.encode(zip_data.getvalue(), "base64").decode()
    with open(str(file_name), "w") as file_object:
        file_object.write(zip_conv)


def main():
    """CLI Entrypoint for generating seeds."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--settings_string", help="The settings string to use to generate a seed", required=False)
    parser.add_argument("--json_data", help="The json data to use to generate a seed", required=False)
    parser.add_argument("--preset", help="Preset to use", required=False)
    parser.add_argument("--output", help="File to name patch file", required=True)
    parser.add_argument("--seed", help="Seed ID to use", required=False)
    args = parser.parse_args()
    print("This file is disabled till further notice.")
    sys.exit(1)
    if args.json_data is None:
        if args.settings_string is not None:
            try:
                setting_data = decrypt_settings_string_enum(args.settings_string)
            except Exception:
                print("Invalid settings String")
                sys.exit(2)
        elif args.preset is not None:
            presets = json.load(open("static/presets/preset_files.json"))
            found = False
            for file in presets:
                with open("static/presets/" + file, "r") as preset_file:
                    data = json.load(preset_file)
                    if args.preset == data.get("name"):
                        setting_data = default
                        for key in data:
                            setting_data[key] = data[key]
                        setting_data.pop("name")
                        setting_data.pop("description")
                        found = True
            if found is False:
                sys.exit(2)
        if args.seed is not None:
            setting_data["seed"] = args.seed
        else:
            setting_data["seed"] = random.randint(0, 100000000)
    else:
        print(args.json_data)
        setting_data = json.loads(str(args.json_data))
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
                setting_data[k] = SettingsMap[k][v]
    try:
        generate(setting_data, args.output)
    except Exception as e:
        if os.environ.get("HOSTED_SERVER") is not None:
            error_table = dynamodb.Table("dk64_error_db")
            error_table.put_item(
                Item={
                    "time": str(time.time()),
                    "error_data": str(traceback.format_exc()),
                }
            )
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
