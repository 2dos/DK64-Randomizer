"""Add all relevant wiki HTML pages."""

import os
import json
from enum import IntEnum, auto


class CamelCaseState(IntEnum):
    """Camel Case State enum."""

    null = auto()
    lower = auto()
    upper = auto()
    space = auto()
    number = auto()


def getNameFromCamelSnakeCase(text: str):
    """Convert camel or snake case text into regular text."""
    if " " in text:
        # Assume it has spaces inside, return text
        return text
    # Handle Snake Case
    text = text.replace("_", " ")
    # Handle Camel Case
    last_state = CamelCaseState.null
    output_string = ""
    for char in text:
        if char == " ":
            last_state = CamelCaseState.space
            output_string += char
        elif char.isnumeric():
            if last_state == CamelCaseState.lower:
                output_string += " "
            output_string += char
            last_state = CamelCaseState.number
        elif char == char.upper():
            if last_state in (CamelCaseState.lower, CamelCaseState.number):
                output_string += " "
            output_string += char
            last_state = CamelCaseState.upper
        elif char == char.lower():
            output_string += char
            last_state = CamelCaseState.lower
        else:
            output_string += char
            last_state = CamelCaseState.null
    return output_string


def createArticleJSON(file_heads: list):
    """Create JSON file containing all articles."""
    with open("./wiki/articles.json", "w") as fh:
        fh.write(json.dumps([{"name": getNameFromCamelSnakeCase(x), "link": x} for x in file_heads], indent=4))


def createHTML(markdown_file_name: str, markdown_path: str, template_text: str):
    """Create the relevant HTML file for a markdown entry."""
    file_head = markdown_file_name.split(".")[0]
    entry_name = file_head
    html_file_name = f"{file_head}.html"
    html_text = template_text.replace("<title></title>", f"<title>{getNameFromCamelSnakeCase(entry_name)}</title>")
    html_text = template_text.replace("<title></title>", f"<title>{getNameFromCamelSnakeCase(entry_name)}</title>")
    html_text = template_text.replace('<h1 id="page-title"></h1>', f'<h1 id="page-title">{getNameFromCamelSnakeCase(entry_name)}</h1>')
    html_text = html_text.replace('<div id="markdown_content"></div>', f"<div id=\"markdown_content\" ref=\"{markdown_path.replace('./','./article_markdown/')}\"></div>")
    with open(f"./wiki/{html_file_name}", "w") as fh:
        fh.write("<!-- DON'T EDIT THIS FILE. EDIT template.html INSTEAD -->\n")
        fh.write(html_text)


items = []
ARTICLE_DIRECTORY = "./wiki/article_markdown"
for path, subdirs, files in os.walk(ARTICLE_DIRECTORY):
    for name in files:
        if ".md" in name:
            items.append(os.path.join(path, name).replace(ARTICLE_DIRECTORY, ".").replace("\\", "/"))
template_text = None
with open("./wiki/template.html", "r") as fh:
    template_text = fh.read()
if template_text is not None:
    for item in items:
        createHTML(item.split("/")[-1], item, template_text)
    createArticleJSON([item.split("/")[-1].split(".")[0] for item in items])
