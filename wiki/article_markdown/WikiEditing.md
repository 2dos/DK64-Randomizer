The content in the Donkey Kong 64 Randomizer wiki is written using [markdown](https://www.markdownguide.org/), and then converting those files into HTML output through [ShowdownJS](https://showdownjs.com/). The output is then modified to introduce stylings to improve legitibility and overall user experience.

# Adding a page to the wiki
To create a wiki article, create a file within `./wiki/article_markdown` on the [DK64 Randomizer GitHub repo](https://github.com/2dos/DK64-Randomizer). The file must be titled as the name of your article. You can choose from one of the following naming conventions:
- Using spaces
- CamelCase
- snake_case

The file can be placed within a subdirectory of `./wiki/article_markdown` if you so wish for organization purposes, but it **MUST** not match the filename of any other markdown file in the `./wiki/article_markdown` directories and all subdirectories within that. Otherwise one will override another.

# Producing the HTML file
To produce the HTML file which contains all of the necessary stylings, you will need to run:
```
python ./update_wiki.py
```
or the `Lint Repo` task on VSCode. This will update all HTML files to include their markdown file inside, as well as include any updated styling choices.

# Editing the template file
The template used for all wiki articles excluding the homepage of the wiki is held within `./wiki/template.html` and is slightly modified by `./update_wiki.py`.

> **WARNING**: In modifying either file, it is likely going to result in changes to all wiki article html files. Please ensure any changes made do not negatively impact existing articles.

# Custom Elements and behavior
To achieve a balance between the simplicity of creating markdown files, the ability to standardize the look and interactions of a website and the customization of HTML, there are various custom HTML elements which are coded into the template that the parser will pick up on.

## Content Navigation Menu
A table of contents will be automatically generated based on the headers of your markdown file (Anything preceded by a certain amount of `#` characters). Your markdown file cannot skip any levels of headers. For example, you cannot have a markdown file which has `# `, `## ` and `#### `, but not `### `. This also means that if you have headers, you **MUST** have at least one header preceded by `# `.

## Pre-navigation summary
Any text which precedes the first `# text` header, if there is one present in the markdown file will appear above the navigation menu. Use this space to give a quick summary of what the article is about.

## Embedded YouTube Videos
To include an embedded YouTube link, you will need to add the following piece of code to your markdown file:
```
<ytvideo yt-id="RFZzMbI-mSo"></ytvideo>
```

This will be converted to the following:

<ytvideo yt-id="RFZzMbI-mSo"></ytvideo>