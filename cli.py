from operator import setitem
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler
import random
import codecs
import json
import pickle
import argparse
from randomizer.SettingStrings import decrypt_setting_string

def generate(generate_settings):
    settings = Settings(generate_settings)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    encoded = codecs.encode(pickle.dumps(spoiler), "base64").decode()
    print(encoded)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--settings_string", help="The settings string to use to generate a seed", required=False)
    parser.add_argument("--preset", help="Preset to use", required=False)
    args = parser.parse_args()
    if args.settings_string is not None:
        decrypt_setting_string(args.settings_string)
        try:
            setting_data = decrypt_setting_string(args.settings_string)
        except Exception:
            print("Invalid settings String")
    elif args.preset is not None:
        presets = json.load(open('static/presets/preset_files.json'))
        default = json.load(open('static/presets/default.json'))
        for file in presets.get("progression"):
            with open('static/presets/' + file, 'r') as preset_file:
                data = json.load(preset_file)
                if args.preset == data.get("name"):
                    setting_data = default
                    for key in data:
                        setting_data[key] = data[key]
                    setting_data.pop("name")
                    setting_data.pop("description")
                    print(setting_data)
    setting_data["seed"] = random.randint(0, 100000000)
    generate(setting_data)

if __name__ == '__main__':
    main()



