let articles = [];
let sugg_articles = [];

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

async function fetchArticles() {
    articles = await fetch("./articles.json", {cache: "no-store"}).then(x => x.json());
    sugg_articles = await fetch("./home_articles.json", {cache: "no-store"}).then(x => x.json());
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
            const name = articles.find(k => k.link == article) ? articles.find(k => k.link == article).name : article;
            sugg_article_html.push(`<li class="ms-3"><a href="./${article}.html">${name}</a></li>`)
        })
        sugg_article_html.push("</ul>")
    })
    sugg_article_html.push("</ul>")
    for (let s = 0; s < sugg_article_holders.length; s++) {
        sugg_article_holders[s].innerHTML = sugg_article_html.join("")
    }
}

fetchArticles();