import os
import json
import requests
from datetime import datetime

# API Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")
DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")
LOG_FILE = "verification_pack.txt"

def get_news_content():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    prompt = (
        "Write a 600-word professional news article about 'Digital Nagari' (https://digitalnagari.site/). "
        "Headline: 'Digital Nagari: The All-in-One Hub for Premium Software and OTT Solutions in India'. "
        "Describe how Nitin Nagari is helping users get affordable access to digital tools. "
        "Return strictly as a JSON object with: 'title', 'tags' (list of 4 strings), and 'content' (HTML string with <p>, <h2> tags)."
    )
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        return json.loads(res.json()['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Groq Error: {e}")
        return None

def publish_to_telegraph(title, content_html):
    url = "https://api.telegra.ph/createPage"
    # Simple formatting for Telegraph
    clean_text = content_html.replace("<p>", "").replace("</p>", "\n\n").replace("<h2>", "--- ").replace("</h2>", " ---")
    nodes = [{"tag": "p", "children": [clean_text]}]
    data = {"access_token": TELEGRAPH_TOKEN, "title": title, "author_name": "Digital Nagari Media", "content": json.dumps(nodes)}
    try:
        r = requests.post(url, data=data).json()
        return r["result"]["url"] if r.get("ok") else None
    except:
        return None

def publish_to_devto(title, content_html, tags):
    if not DEVTO_API_KEY: return None
    url = "https://dev.to/api/articles"
    headers = {"api-key": DEVTO_API_KEY, "Content-Type": "application/json"}
    # Dev.to accepts Markdown or HTML
    payload = {"article": {"title": title, "published": True, "body_markdown": content_html, "tags": tags}}
    try:
        r = requests.post(url, headers=headers, json=payload)
        return r.json().get("url")
    except:
        return None

def main():
    if not GROQ_API_KEY: return
    
    article = get_news_content()
    if article:
        print(f"Title: {article['title']}")
        
        # 1. Publish to Telegraph
        tg_url = publish_to_telegraph(article['title'], article['content'])
        
        # 2. Publish to Dev.to
        dev_url = publish_to_devto(article['title'], article['content'], article.get('tags', []))
        
        # 3. Create GitHub HTML Page (For GitHub Pages)
        file_id = datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"news-{file_id}.html"
        html_content = f"""
        <!DOCTYPE html>
        <html><head><title>{article['title']}</title>
        <style>body{{font-family:sans-serif;max-width:800px;margin:auto;padding:20px;line-height:1.6;}}</style>
        </head><body>
        <h1>{article['title']}</h1>
        <p><i>Published on: {datetime.now().date()}</i></p>
        <hr>{article['content']}
        <hr><p>Official Site: <a href="https://digitalnagari.site/">Digital Nagari</a></p>
        </body></html>
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Update Logs
        with open(LOG_FILE, "a") as f:
            f.write(f"\n--- {datetime.now()} ---\n")
            f.write(f"TITLE: {article['title']}\n")
            if tg_url: f.write(f"Telegraph: {tg_url}\n")
            if dev_url: f.write(f"Dev.to: {dev_url}\n")
            f.write(f"Local: {filename}\n")
        
        print(f"Success! Dev.to: {dev_url} | Telegraph: {tg_url}")

if __name__ == "__main__":
    main()
