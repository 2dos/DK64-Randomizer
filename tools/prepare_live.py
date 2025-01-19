"""Convert files to their minified types."""

import glob
import os
import re
import json
import shutil
import subprocess
from hashlib import md5
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Load version from version.py
version = None
with open("version.py", "r") as version_file:
    for line in version_file:
        if line.startswith("version"):
            version = line.split("=")[1].strip().strip('"')


def get_files(path, extension, recursive=False):
    """Generate filepaths for each file into path with the target extension."""
    if not recursive:
        for file_path in glob.iglob(path + "/*." + extension):
            yield file_path
    else:
        for root, dirs, files in os.walk(path):
            for file_path in glob.iglob(root + "/*." + extension):
                yield file_path


def find_list_resources(tag, attribute, soup):
    """Find resources based off of their tag and attributes."""
    resources = []
    for x in soup.findAll(tag):
        try:
            resources.append(x[attribute])
        except KeyError:
            pass
    return resources


def compress_jsonc():
    """Combine all JSONC files in the randomizer Enums directory and output to a single JSON file."""
    DIR = "./randomizer/Enums/"
    OUTPUT_FILE = "./static/compiled.jsonc"
    combined_data = {}
    for filename in os.listdir(DIR):
        if filename.endswith(".jsonc"):
            filepath = os.path.join(DIR, filename)
            with open(filepath, "r") as file:
                content = file.read()
                # Strip the comments from the JSONC file
                content = re.sub(r"//.*?\n", "", content)
                content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
                content = json.loads(content)
                combined_data[filename.replace(".jsonc", "")] = content
    with open(OUTPUT_FILE, "w") as output_file:
        json.dump(combined_data, output_file, separators=(",", ":"))


for f in [*get_files(os.getcwd(), "html", recursive=True), *get_files(os.getcwd(), "html", recursive=True)]:
    with open(f, "r") as reader:
        html = reader.read()
        soup = BeautifulSoup(html, features="html.parser")

        image_src = find_list_resources("img", "src", soup)
        script_src = find_list_resources("script", "src", soup)
        css_link = find_list_resources("link", "href", soup)

        # Update HTML file links
        for link in [*css_link, *script_src, *image_src]:
            if "http://" in link or "https://" in link:
                # External link
                pre = ""
                if "wiki/" in f:
                    pre = "."
                file_name = "/web_cache" + urlparse(link).path + urlparse(link).query
                Path(os.getcwd() + os.path.dirname(file_name)).mkdir(parents=True, exist_ok=True)
                req = requests.get(link, allow_redirects=False)
                open(f".{file_name}", "wb").write(req.content)
                html = html.replace(link, f".{pre}{file_name}")
            elif link.endswith(".js"):
                # Local JavaScript file - append version query parameter
                html = html.replace(link, f"{link}?v={version}")

        # Update JavaScript blocks
        pattern = r'(\{ src: [\'"])(\.\/static\/js\/.*?\.js)([\'"], defer: true \})'
        updated_html = re.sub(pattern, rf"\1\2?v={version}\3", html)

        # Write the modified HTML content back to the file
        with open(f, "w") as writer:
            writer.write(updated_html)
# compress_jsonc()
subprocess.run(["python3", "setup.py", "bdist_wheel"])
shutil.copyfile("dist/dk64rando-1.0.0-py3-none-any.whl", "static/py_libraries/dk64rando-1.0.0-py3-none-any.whl")

# Create the file Gemfile
with open("Gemfile", "w") as file:
    file.write(
        """source 'https://rubygems.org'
gem 'github-pages'"""
    )
