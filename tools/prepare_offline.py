"""Convert files to their minified types."""

import glob
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


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
    list = []
    for x in soup.findAll(tag):
        try:
            list.append(x[attribute])
        except KeyError:
            pass
    return list


for f in [*get_files(os.getcwd(), "html", recursive=True), *get_files(os.getcwd(), "html", recursive=True)]:
    with open(f, "r") as reader:
        html: str = reader.read()
        soup = BeautifulSoup(html, features="html.parser")

        image_src = find_list_resources("img", "src", soup)
        script_src = find_list_resources("script", "src", soup)
        css_link = find_list_resources("link", "href", soup)
        for link in [*css_link, *script_src, *image_src]:
            if "http://" in link or "https://" in link:
                file_name = "/web_cache" + urlparse(link).path + urlparse(link).query
                Path(os.getcwd() + os.path.dirname(file_name)).mkdir(parents=True, exist_ok=True)
                req = requests.get(link, allow_redirects=False)
                open(f".{file_name}", "wb").write(req.content)
                html = html.replace(link, f".{file_name}")
                with open(f, "w") as writer:
                    writer.write(html)

# subprocess.run(["css-html-js-minify", "static/styles/", "--overwrite"])
# subprocess.run(["pyminify", "-i", "."])
