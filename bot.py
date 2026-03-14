import os
import json
import requests
from datetime import datetime

# API Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")
DEVTO_API_KEY = os.getenv("DEVTO_API_KEY") # Optional: Dev.to key
LOG_FILE = "verification_pack.txt"

def get_news_content():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    prompt = (
        "Write a professional PR news article about 'Digital Nagari' (https://digitalnagari.site/). "
        "Tone: Journalistic and corporate. Headline: 'Digital Nagari Set to Disrupt the Indian OTT and Software Market'. "
        "Return as JSON with 'title', 'tags' (list), and 'content' (long string with HTML tags like <p> and <h2>)."
    )
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        return json.loads(res.json()['choices'][0]['message']['content'])
    except:
        return None

def publish_to_telegraph(title, content_html):
    # Converts HTML to Telegraph format and publishes
    url = "https://api.telegra.ph/createPage"
    # Simple conversion: wrappping content in nodes
    nodes = [{"tag": "p", "children": [content_html.replace("<p>", "").replace("</p>", "\n")]}]
    data = {"access_token": TELEGRAPH_TOKEN, "title": title, "author_name": "Digital Nagari PR", "content": json.dumps(nodes)}
    try:
        r = requests.post(url, data=data).json()
        return r["result"]["url"] if r.get("ok") else None
    except:
        return None

def publish_to_devto(title, content_html, tags):
    """Publishes to Dev.to (High Authority News)"""
    if not DEVTO_API_KEY: return None
    url = "https://dev.to/api/articles"
    headers = {"api-key": DEVTO_API_KEY, "Content-Type": "application/json"}
    payload = {"article": {"title": title, "published": True, "body_markdown": content_html, "tags": tags}}
    try:
        r = requests.post(url, headers=headers, json=payload)
        return r.json().get("url")
    except:
        return None

def create_github_blog_page(title, content_html):
    """Creates an HTML file in the repo to act as a permanent News Blog"""
    filename = f"news-{datetime.now().strftime('%Y%m%d%H%M')}.html"
    template = f"""
    <html>
    <head><title>{title}</title><style>body{{font-family:sans-serif; line-height:1.6; padding:50px;}}</style></head>
    <body>
        <h1>{title}</h1>
        <hr>
        {content_html}
        <br>
        <p>Published by <a href="https://digitalnagari.site">Digital Nagari</a></p>
    </body>
    </html>
    """
    with open(filename, "w") as f:
        f.write(template)
    return filename

def main():
    if not GROQ_API_KEY: return
    
    article = get_news_content()
    if article:
        # 1. Telegraph
        tg_url = publish_to_telegraph(article['title'], article['content'])
        
        # 2. GitHub Blog Page (Permanent)
        gh_file = create_github_blog_page(article['title'], article['content'])
        
        # 3. Dev.to (Optional)
        dev_url = publish_to_devto(article['title'], article['content'], article.get('tags', []))

        # Saving logs
        with open(LOG_FILE, "a") as f:
            log = f"[{datetime.now()}] TITLE: {article['title']}\n"
            if tg_url: log += f" - Telegraph: {tg_url}\n"
            log += f" - GitHub News: https://mrnitin03.github.io/Groq-AutoAgent/{gh_file}\n"
            if dev_url: log += f" - Dev.to: {dev_url}\n"
            f.write(log + "-"*20 + "\n")
        print("Done!")

if __name__ == "__main__":
    main()
