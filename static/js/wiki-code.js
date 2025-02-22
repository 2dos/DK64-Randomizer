let articles = [];
let sugg_articles = [];

function getSearchScore(find_text, in_text) {
    const instances = in_text.toLowerCase().split(find_text.toLowerCase()).length - 1;
    return (instances * find_text.length) / in_text.length;
}

function highlightInstancesOfText(find_text, in_text) {
    const text_split = in_text.toLowerCase().split(find_text.toLowerCase());
    let global_position = 0;
    let total_text = "";
    text_split.forEach((segment, index) => {
        if (index > 0) {
            total_text += `<strong>${in_text.substring(global_position, global_position + find_text.length)}</strong>`;
            global_position += find_text.length;
        }
        total_text += in_text.substring(global_position, global_position + segment.length);
        global_position += segment.length;
    })
    return total_text;
}

function goTo(url, new_tab=false) {
    if (url.indexOf("./") !== 0) {
        window.location.href = url;
        return;
    }
    const html_index = url.indexOf(".html");
    if (html_index === -1) {
        window.location.href = url;
        return;
    }
    if (html_index === (url.length - 5)) {
        window.location.href = `./index.html?title=${url.substring(2, url.length - 5)}`
        return;
    }
    window.location.href = url;
}

function getLink(item) {
    if (Object.keys(item).includes("github")) {
        return `./index.html?title=${item.github}`
    }
    return `./index.html?title=${item.link}`
}

let article_names = [];
let articles_ready = false;
async function getSuggestions() {
    return new Promise((resolve) => {
        const checkReady = () => {
            if (articles_ready) {
                resolve(article_names.slice());
            } else {
                setTimeout(checkReady, 100);
            }
        };
        checkReady();
    })
}

async function fetchArticles() {
    articles = await fetch("./articles.json", {cache: "no-store"}).then(x => x.json());
    sugg_articles = await fetch("./home_articles.json", {cache: "no-store"}).then(x => x.json());
    // Populate search suggestions
    article_names = articles.map(item => {
        return {
            "name": item.name,
            "link": getLink(item),
        };
    });
    articles_ready = true;
    // Populate Suggested Article Text
    const sugg_article_holders = document.getElementsByClassName("sugg-articles");
    if (sugg_article_holders.length == 0) {
        return;
    }
    let sugg_article_html = ["<ul class=\"list-inline\">"]
    sugg_articles.forEach(item => {
        sugg_article_html.push(`<li>${item.head}</li>`)
        sugg_article_html.push("<ul class=\"list-inline\">")
        item.articles.forEach(article => {
            const art_data = articles.find(k => k.link == article);
            const name = art_data ? art_data.name : article;
            let link = null;
            if (art_data) {
                link = getLink(art_data);
            }
            if (link != null) {
                sugg_article_html.push(`<li class="ms-3"><a href="${link}">${name}</a></li>`)
            }
        })
        sugg_article_html.push("</ul>")
    })
    sugg_article_html.push("</ul>")
    for (let s = 0; s < sugg_article_holders.length; s++) {
        sugg_article_holders[s].innerHTML = sugg_article_html.join("")
    }
}

fetchArticles();

const invalid_id_characters = [" ", ",", "\"", "'"]
let used_ids = {};

class MarkdownNavItem {
    constructor(text, indent_level) {
        this.text = text;
        // Construct id
        let split_id = text.toLowerCase().split("")
        let new_split_id = []
        split_id.forEach((char, char_index) => {
            let new_char = char;
            if (invalid_id_characters.includes(char)) {
                new_char = "-";
            }
            new_split_id.push(new_char);
        })
        let id = new_split_id.join("");
        if (Object.keys(used_ids).includes(id)) {
            used_ids[id] += 1;
            id = `${id}-${used_ids[id]}`
        } else {
            used_ids[id] = 0;
        }
        this.id = id;
        this.indent_level = indent_level;
    }
}

const markdown_headers = [1, 2, 3, 4, 5].map(item => `${"#".repeat(item)} `);

function getListItemFromEntry(entry) {
    return `<li>
        <a href=\"#${entry.id}\" class='list_number'>${entry.numeric}</a>
        <a href=\"#${entry.id}\" class='list_header'> ${entry.text}</a>
    </li>`
}

function populateNavigation(markdown) {
    let entries = [];
    lines = markdown.split("\n")
    lines.forEach(line => {
        let indent_level = null;
        markdown_headers.forEach((header, index) => {
            if (line.substring(0, header.length) == header) {
                indent_level = index;
            }
        })
        if (indent_level != null) {
            let start = line.substring(markdown_headers[indent_level].length);
            start = start.split("").filter(item => item != "\r").join("");
            entries.push(new MarkdownNavItem(start, indent_level))
        }
    })
    let nav_entries = [];
    let html_data = [];
    let indentation_levels = Array(markdown_headers.length).fill(-1);
    entries.forEach(entry => {
        indentation_levels[entry.indent_level] += 1;
        if (indentation_levels[entry.indent_level] == 0) {
            html_data.push(`<ul${entry.indent_level == 0 ? ' style=\"padding-left:0px\"' : ''}>`)
        }
        for (let i = entry.indent_level + 1; i < markdown_headers.length; i++) {
            if (indentation_levels[i] != -1) {
                html_data.push("</ul>")
            }
            indentation_levels[i] = -1;
        }
        let numeric = "";
        let has_hit_limit = false;
        indentation_levels.forEach(indent => {
            if (!has_hit_limit) {
                if (indent < 0) {
                    has_hit_limit = true;
                } else {
                    numeric += `${indent + 1}.`
                }
            }
        })
        entry.numeric = numeric.substring(0, numeric.length - 1);
        if (entry.indent_level == 0) {
            html_data.push(getListItemFromEntry(entry))
            nav_entries.push({
                "head": entry,
                "sub": [],
            })
        } else {
            data = nav_entries;
            for (let i = 0; i < entry.indent_level; i++) {
                data = data[indentation_levels[i]].sub;
            }
            html_data.push(getListItemFromEntry(entry))
            data.push({
                "head": entry,
                "sub": [],
            })
        }
    })
    indentation_levels.forEach(indent => {
        if (indent != -1) {
            html_data.push("</ul>")
        }
    })
    document.getElementById("markdown_navigation").innerHTML = html_data.join("")
    html_data[0] += `<li><a href=\"#page-top\" class='list_header'>(top)</a></li>`
    document.getElementById("markdown_navigation_sidebar").innerHTML = html_data.join("")
    if (html_data.length > 20) { // Mitigates overflow issues since scrolling + sticky doesn't work so well together
        document.getElementById("markdown_navigation_sidebar").classList.add("truncate_sidebar_scroll");
    }
}

function dateDiffInDays(a, b) {
    const _MS_PER_DAY = 1000 * 60 * 60 * 24;
    // Discard the time and time-zone information.
    const utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
    const utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());

    return Math.floor((utc2 - utc1) / _MS_PER_DAY);
}

const copyContent = async (text) => {
    try {
        await navigator.clipboard.writeText(text);
        console.log('Content copied to clipboard');
    } catch (err) {
        console.error('Failed to copy: ', err);
    }
}

FIX_FLEX = true;
FIX_HEADERS = false;

function fixHeaders(text) {
    // Fix flex containers
    if (FIX_FLEX) {
        if (text.includes("<flex>")) {
            const segments = text.split("<flex>");
            let new_segments = [];
            segments.forEach(segment => {
                if (segment.includes("</flex>")) {
                    const subsegments = segment.split("</flex>");
                    const new_subseg = subsegments.map((item, index) => {
                        if (index < (subsegments.length - 1)) {
                            return item.replaceAll("\n","");
                        }
                        return item;
                    })
                    new_segments.push(new_subseg.join("</flex>"))
                } else {
                    new_segments.push(segment)
                }
            })
            text = new_segments.join("<flex>");
        }
    }
    // Fix Headers
    if (FIX_HEADERS) {
        let split_text = text.split("\n");
        let header_lines = []
        split_text.forEach((line, line_index) => {
            const trimmed = line.trim()
            let header_data = null;
            markdown_headers.forEach((head, header_index) => {
                if (trimmed.substring(0, head.length) == head) {
                    same_as_last = false
                    if (header_lines.length > 0) {
                        if (header_index == header_lines[header_lines.length - 1].power) {
                            same_as_last = true;
                        }
                    }
                    header_data = {
                        "index": line_index,
                        "line": trimmed,
                        "power": header_index,
                        "same_as_last": same_as_last
                    }
                }
            })
            if (header_data != null) {
                header_lines.push(header_data)
            }
        })
        console.log(header_lines)
    }
    return text;
}

async function filterMarkdown(element, converter) {
    let last_modified = null;
    let text = await fetch(element.getAttribute("ref"), {cache: "no-store"}).then(x => {
        last_modified = x.headers.get("Last-Modified");
        return x.text()
    });
    text = fixHeaders(text);
    // Last Modified Date
    const last_modified_hook = document.getElementById("last-modified");
    if (last_modified == null) {
        last_modified_hook.remove();
    } else {
        const modified_date = new Date(last_modified);
        const current_date = new Date();
        const diff = dateDiffInDays(modified_date, current_date);
        let diff_text = "Unknown"
        if (diff == 0) {
            diff_text = "Today"
        } else {
            diff_text = `${diff} day${diff == 1 ? '' : 's'} ago`
        }
        last_modified_hook.innerText = `Last Modified: ${diff_text}`;
    }
    // Handle summative starting text
    const primary_header_finder = "\n# "
    let has_summary = false;
    if (text.substring(0, 2) != "# ") { // Ensure that this doesn't happen if the first line is a header
        if (text.includes("\n# ")) {
            // Includes primary header
            let splitter = text.indexOf(primary_header_finder)
            if (splitter > -1) {
                const summation = text.substring(0, splitter)
                text = text.substring(splitter)
                document.getElementById("content-summary").innerHTML = converter.makeHtml(summation);
                has_summary = true;
            }
        }
    }
    if (!has_summary) {
        document.getElementById("content-summary").remove();
    }
    // Populate HTML
    populateNavigation(text);
    return text;
}

const markdown_filters = {
    "</h2>": "</h2><hr />",
    "<table>": "<table class=\"table table-dark table-hover\" style=\"max-width:100%\">",
    "<pre>": "<div class=\"code-copy-container\"><pre>",
    "</pre>": "</pre><div><div class=\"code-copy p-1 m-1\"><a title=\"Copy Code\" onClick=\"copyCode(this)\"><i class=\"fa-regular fa-lg fa-copy\"></i></a></div></div></div>"
}

function filterHTML(element, output_html) {
    Object.keys(markdown_filters).forEach(k => {
        output_html = output_html.replaceAll(k, markdown_filters[k]);
    })
    element.innerHTML = output_html;
    element.removeAttribute("ref");
    document.getElementById("content-pane").removeAttribute("hidden");
    // Content Filtration
    const content_hook = document.getElementById("markdown_content");
    // Add classes to code blocks where their parent element isn't a pre-tag
    const code_elements = content_hook.getElementsByTagName("code");
    for (let c = 0; c < code_elements.length; c++) {
        if (code_elements[c].parentElement.tagName.toLowerCase() != "pre") {
            code_elements[c].classList.add("inline-code");
        }
    }

    // Parse custom elements
    // YouTube Videos (<ytvideo yt-id="12345678-0"></ytvideo>)
    const yt_videos = content_hook.getElementsByTagName("ytvideo");
    while (yt_videos.length > 0) {
        const yt_id = yt_videos[0].getAttribute("yt-id");
        yt_videos[0].outerHTML = `<div style="text-align:center"><iframe width="420" height="315" src="https://www.youtube.com/embed/${yt_id}"></iframe></div>`
    }
    for (let y = 0; y < yt_videos.length; y++) {
    }
    // Image Buttons (<imgbtn img="link" href="link" text="text"></imgbtn>)
    const img_buttons = content_hook.getElementsByTagName("imgbtn");
    while (img_buttons.length > 0) {
        const btn_img = img_buttons[0].getAttribute("img");
        const btn_href = img_buttons[0].getAttribute("href");
        const btn_text = img_buttons[0].getAttribute("text");
        img_buttons[0].outerHTML = `<div class="img-btn-container p-3 m-2 user-select-none" onclick="goTo('${btn_href}')"><img src=${btn_img} /><div class="img-btn-text">${btn_text}</div></div>`
    }
    // Image Info
    const image_info = content_hook.getElementsByTagName("imginfo");
    while (image_info.length > 0) {
        const info_img = image_info[0].getAttribute("img");
        const has_text = image_info[0].hasAttribute("text");
        const info_text = image_info[0].getAttribute("text");
        const has_header = image_info[0].hasAttribute("header");
        const info_header = image_info[0].getAttribute("header");
        const has_subtitle = image_info[0].hasAttribute("subtitle");
        const info_subtitle = image_info[0].getAttribute("subtitle");
        image_info[0].outerHTML = `
            <div class="card mx-2" style="width: 18rem;">
                <img src=${info_img} class="card-img-top" alt="${info_text}" />
                <div class="card-body">
                    ${has_header ? `
                        <h5 class="card-title">${info_header}</h5>
                    ` : ""}
                    ${has_subtitle ? `
                        <h6 class="card-subtitle mb-2 text-body-secondary">${info_subtitle}</h6>
                    ` : ""}
                    ${has_text ? `
                        <p class="card-text">${info_text}</p>
                    ` : ""}
                    </p>
                </div>
            </div>`
    }
    // Font-Awesome icons <fa-icon>cls</fa-icon>
    const fa_icons = content_hook.getElementsByTagName("fa-icon");
    while (fa_icons.length > 0) {
        const classes = fa_icons[0].getAttribute("class");
        fa_icons[0].outerHTML = `<i class="${classes} ms-3"></i>`
    }
    // Flex <flex></flex>
    const flex_items = content_hook.getElementsByTagName("flex");
    while (flex_items.length > 0) {
        const contents = flex_items[0].innerHTML;
        flex_items[0].outerHTML = `<div style="display:flex">${contents}</div>`
    }

    // BS Alerts
    const alert_types = {
        "primary": "fa-solid fa-circle-info",
        "secondary": "fa-solid fa-circle-info",
        "success": "fa-solid fa-circle-check",
        "danger": "fa-solid fa-triangle-exclamation",
        "warning": "fa-solid fa-triangle-exclamation",
        "info": "fa-solid fa-circle-info",
        "light": "",
        "dark": "",
    };
    Object.keys(alert_types).forEach(al_type => {
        const info_items = content_hook.getElementsByTagName(`alert${al_type}`);
        while (info_items.length > 0) {
            const contents = info_items[0].innerHTML;
            info_items[0].outerHTML = `
                <div class="alert alert-${al_type}" role="alert">
                    <i class="${alert_types[al_type]}"></i>
                    ${contents}
                </div>`
        }
    })

    // Warp to ID if specified
    hash = window.location.hash;
    if (hash.length > 0) {
        let hash_hook = null;
        if (hash.substring(0, 1) == "#") {
            hash_hook = document.getElementById(hash.substring(1))
        } else {
            hash_hook = document.querySelector(hash);
        }
        if (hash_hook) {
            hash_hook.scrollIntoView();
        }
    }

    const imgs = document.getElementsByTagName("img");
    for (let i = 0; i < imgs.length; i++) {
        if (imgs[i].parentElement.classList.contains("img-btn-container")) {
            continue;
        }
        imgs[i].addEventListener("click", (e) => {
            const alt_text = e.target.getAttribute("alt");
            updateImage(e.target.getAttribute("src"), alt_text == "image" ? "" : alt_text);
        });
    }

    // Modify links
    const links = document.getElementsByTagName("a");
    for (let i = 0; i < links.length; i++) {
        href = links[i].getAttribute("href");
        if (href) {
            if (href.substring(0, 2) == "./") {
                console.log("Modifying link...");
                links[i].setAttribute("href", `?title=${href.substring(2)}`)
            }
        }
    }
}