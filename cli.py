"""CLI script for running seed generation."""
import argparse
import codecs
import json
import pickle
import random
import os
import sys
import traceback

from randomizer.Enums.Settings import SettingsMap
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Spoiler import Spoiler


def generate(generate_settings, file_name, gen_spoiler):
    """Gen a seed and write the file to an output file."""
    settings = Settings(generate_settings)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    if gen_spoiler:
        with open(file_name + "-spoiler.json", "w") as outfile:
            outfile.write(spoiler.json)
    encoded = codecs.encode(pickle.dumps(spoiler), "base64").decode()
    with open(file_name + ".lanky", "w") as outfile:
        outfile.write(encoded)


def main():
    """CLI Entrypoint for generating seeds."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--settings_string", help="The settings string to use to generate a seed", required=False)
    parser.add_argument("--preset", help="Preset to use", required=False)
    parser.add_argument("--output", help="File to name patch file", required=True)
    parser.add_argument("--seed", help="Seed ID to use", required=False)
    parser.add_argument("--generate_spoiler", help="Dumps the Spoiler log to a file along with the patch file.", required=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    if not os.environ.get("POST_BODY"):
        if args.settings_string is not None:
            try:
                setting_data = decrypt_settings_string_enum(args.settings_string)
            except Exception:
                print("Invalid settings String")
                sys.exit(2)
        elif args.preset is not None:
            presets = json.load(open("static/presets/preset_files.json"))
            default = json.load(open("static/presets/default.json"))
            found = False
            for file in presets.get("progression"):
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
        setting_data = json.loads(os.environ.get("POST_BODY"))
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
        generate(setting_data, args.output, args.generate_spoiler)
    except Exception as e:
        with open("error.log", "w") as file_object:
            file_object.write(repr(e))
        with open("traceback.log", "w") as file_object:
            file_object.write(str(traceback.format_exc()))
        print(traceback.format_exc())
        if os.environ.get("DISCORD_WEBHOOK"):
            from discord_webhook import DiscordWebhook, DiscordEmbed

            webhook = DiscordWebhook(url=os.environ.get("DISCORD_WEBHOOK"))
            embed = DiscordEmbed(title="Error Generating Seed", description=str(traceback.format_exc()), color="800020")
            embed.set_timestamp()
            webhook.add_embed(embed)
            webhook.execute()
        sys.exit(1)


if __name__ == "__main__":
    main()
