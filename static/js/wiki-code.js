const invalid_id_characters = [" ", ",", "(", ")", "."]
let used_ids = {};

class MarkdownNavItem {
    constructor(text, indent_level) {
        this.text = text;
        // Construct id
        let id = text.toLowerCase().split("").filter(item => !invalid_id_characters.includes(item)).join("");
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

let articles = [];

function getSearchScore(find_text, in_text) {
    return in_text.toLowerCase().split(find_text.toLowerCase()).length - 1;
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
    window.location.href = url;
}

function handleSuggestionClick(url) {
    document.getElementById("search_suggestions").innerHTML = "";
    document.getElementById("article-search").value = "";
    goTo(url);
}

document.getElementById("article-search").addEventListener("keyup", (e) => {
    const input_value = e.target.value;
    if (articles.length == 0) {
        return; // No articles
    }
    let matches = [];
    if (input_value.length >= 1) {
        articles.forEach(article => {
            const score = getSearchScore(input_value, article.name);
            if (score > 0) {
                matches.push({
                    "score": score,
                    "text": highlightInstancesOfText(input_value, article.name),
                    "link": `./${article.link}.html`,
                })
            }
        })
        matches = matches.sort((a, b) => a.score > b.score ? 1 : ((b.score > a.score) ? -1 : 0));
    }
    matches = matches.filter((item, index) => index < 5); // Clamp to 5 search results at most
    const sugg_hook = document.getElementById("search_suggestions");
    sugg_hook.innerHTML = matches.map(item => `
        <div class="search-item user-select-none p-2" onclick="handleSuggestionClick('${item.link}')">
            ${item.text}
        </div>
    `).join("");
    const top_offset = e.target.clientTop + e.target.clientHeight;
    const left_offset = e.target.clientLeft;
    sugg_hook.style.top = `calc(${top_offset}px + 0.5rem)`;
    sugg_hook.style.right = `calc(${left_offset}px + 0.5rem)`;
    sugg_hook.style["min-width"] = `${e.target.clientWidth}px`;
})

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

function toggleSidebarCollapse(element) {
    const nav_hook = document.getElementById("markdown_navigation_sidebar");
    const hidden = nav_hook.getAttribute("hidden") != null;
    if (hidden) {
        nav_hook.removeAttribute("hidden");
        element.classList.remove("collapsed");
    } else {
        nav_hook.setAttribute("hidden", "hidden");
        element.classList.add("collapsed");
    }
}

function copyCode(element) {
    const parent = element.parentElement.parentElement.parentElement;
    if (!parent) {
        return;
    }
    const code_blocks = parent.getElementsByTagName("code");
    if (code_blocks.length == 0) {
        return;
    }
    const copyText = code_blocks[0].innerText;
    copyContent(copyText);
    if (!parent.classList.contains("pulse")) {
        if (!parent.classList.contains("pulse_display")) {
            parent.classList.add("pulse");
            parent.classList.add("pulse_display");
            setTimeout(() => {
                parent.classList.remove("pulse");
            }, 300);
            setTimeout(() => {
                parent.classList.remove("pulse_display");
            }, 1000);
        }
    }
}

const markdown_filters = {
    "</h2>": "</h2><hr />",
    "<table>": "<table class=\"table table-dark table-hover\">",
    "<pre>": "<pre><div><div class=\"code-copy\"><a title=\"Copy Code\" onClick=\"copyCode(this)\"><i class=\"fa-regular fa-lg fa-copy\"></i></a></div></div>"
}

async function alterMarkdown(element) {
    const converter = new showdown.Converter({tables: true, headerLevelStart: 2, strikethrough: true});
    let last_modified = null;
    let text = await fetch(element.getAttribute("ref"), {cache: "no-store"}).then(x => {
        last_modified = x.headers.get("Last-Modified");
        return x.text()
    });
    articles = await fetch("./articles.json", {cache: "no-store"}).then(x => x.json());
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
    let output_html = converter.makeHtml(text);
    Object.keys(markdown_filters).forEach(k => {
        output_html = output_html.replaceAll(k, markdown_filters[k]);
    })
    element.innerHTML = output_html;
    element.removeAttribute("ref");
    // Content Filtration
    const content_hook = document.getElementById("markdown_content");
    // Add classes to code blocks where their parent element isn't a pre-tag
    const code_elements = content_hook.getElementsByTagName("code");
    for (let c = 0; c < code_elements.length; c++) {
        if (code_elements[c].parentElement.tagName.toLowerCase() != "pre") {
            code_elements[c].classList.add("inline-code");
        }
    }


    // Parse custom elements - YouTube Videos (<ytvideo yt-id="12345678-0"></ytvideo>)
    const yt_videos = content_hook.getElementsByTagName("ytvideo");
    for (let y = 0; y < yt_videos.length; y++) {
        const yt_id = yt_videos[y].getAttribute("yt-id");
        yt_videos[y].outerHTML = `<iframe width="420" height="315" src="https://www.youtube.com/embed/${yt_id}"></iframe>`
    }

    // Warp to ID if specified
    hash = window.location.hash;
    if (hash.length > 0) {
        const hash_hook = document.querySelector(hash);
        if (hash_hook) {
            hash_hook.scrollIntoView();
        }
    }
}
alterMarkdown(document.getElementById("markdown_content"));

function hideContent(e) {
    const content = document.getElementById("markdown_navigation");
    const content_hr = document.getElementById("content_hr")
    const hidden = content.getAttribute("hidden") != null;
    if (hidden) {
        e.innerText = "Hide";
        content.removeAttribute("hidden");
        content_hr.removeAttribute("hidden");
    } else {
        e.innerText = "Show";
        content.setAttribute("hidden", "hidden");
        content_hr.setAttribute("hidden", "hidden");
    }
}