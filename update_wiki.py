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


ARTICLE_JSON = "./wiki/articles.json"
GH_ARTICLE_JSON = "./wiki/github_articles.json"
NAME_HEADS = ["Custom Locations", "Random Settings"]


def convertName(name: str):
    """Convert name for title purposes."""
    name = getNameFromCamelSnakeCase(name)
    for head in NAME_HEADS:
        if name[: len(head)] == head and len(name) > len(head):
            name = f"{head}:{name[len(head):]}"
    return name


def createArticleJSON(data: list):
    """Create JSON file containing all articles."""
    with open(ARTICLE_JSON, "w") as fh:
        fh.write(json.dumps(data, indent=4))


def createHTML(markdown_data: dict, template_text: str):
    """Create the relevant HTML file for a markdown entry."""
    pretty_name = markdown_data["name"]
    file = markdown_data.get("path", None)
    html_file_name = markdown_data.get("link", None)
    if file is not None:
        file = markdown_data["path"].replace("./", "./article_markdown/")
    if "github" in markdown_data:
        file = f"./index.html?title={markdown_data['github']}"
        html_file_name = markdown_data["github"]
    if html_file_name is not None:
        html_text = template_text.replace("<title></title>", f"<title>{pretty_name}</title>")
        html_text = html_text.replace('<meta content="" property="og:title" />', f'<meta content="{pretty_name}" property="og:title" />')
        html_text = html_text.replace('<h1 id="page-title"></h1>', f'<h1 id="page-title">{pretty_name}</h1>')
        if "github" in markdown_data:
            html_text = html_text.replace(
                '<script id="redirect_handler"></script>',
                f'<script id="redirect_handler">window.location.href="{file}";</script>',
            )
        else:
            html_text = html_text.replace('<div id="markdown_content"></div>', f'<div id="markdown_content" ref="{file}"></div>')
            html_text = html_text.replace('<script id="redirect_handler"></script>', "")
        with open(f"./wiki/{html_file_name}.html", "w") as fh:
            fh.write("<!-- DON'T EDIT THIS FILE. EDIT template.html INSTEAD -->\n")
            fh.write(html_text)


def updateWikiProcedure():
    """Update procedure."""
    items = []
    articles = []
    with open(GH_ARTICLE_JSON, "r") as fh:
        items = json.loads(fh.read())
        articles = items.copy()
    # Generate Paths
    ARTICLE_DIRECTORY = "./wiki/article_markdown"
    for path, subdirs, files in os.walk(ARTICLE_DIRECTORY):
        for name in files:
            if ".md" in name.lower():
                pth = os.path.join(path, name).replace(ARTICLE_DIRECTORY, ".").replace("\\", "/")
                pretty_name = name.split("/")[-1].split(".")[0]
                itm_data = {"name": convertName(pretty_name), "link": pretty_name}
                articles.append(itm_data)
                items.append(itm_data.copy())
                for item in items:
                    if "link" in item:
                        if f"{item['link'].lower()}.md" in pth.lower():
                            item["path"] = pth
    template_text = None
    with open("./wiki/template.html", "r") as fh:
        template_text = fh.read()
    if template_text is not None:
        createArticleJSON(articles)
        for item in items:
            # print(item)
            createHTML(item, template_text)
    print("Wiki Updated")


updateWikiProcedure()
