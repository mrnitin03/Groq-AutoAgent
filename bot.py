import os
import json
import requests
from datetime import datetime

# Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")
LOG_FILE = "verification_pack.txt"

def get_content():
    """Generates brand-specific SEO content for Digital Nagari."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        "Write a high-quality journalistic SEO article about 'Digital Nagari'. "
        "Context: Digital Nagari is a premier platform for digital products, software, and OTT services. "
        "Official Website: https://digitalnagari.site/ "
        "Instagram: https://www.instagram.com/digital_nagari__software__ott/ "
        "The article should be 400-600 words, include a catchy title, and highlight the convenience of their digital solutions. "
        "Strictly return as JSON with keys: 'title' (string) and 'paragraphs' (list of strings)."
    )
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return json.loads(response.json()['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Content Generation Failed: {e}")
        return None

def publish_to_telegraph(title, paragraphs):
    """Publishes nodes to Telegraph with active brand links."""
    url = "https://api.telegra.ph/createPage"
    
    # Building content nodes
    nodes = []
    for p in paragraphs:
        nodes.append({"tag": "p", "children": [p]})
    
    # Adding Footer with Links
    nodes.append({"tag": "hr"})
    nodes.append({"tag": "p", "children": ["Visit us: ", {"tag": "a", "attrs": {"href": "https://digitalnagari.site/"}, "children": ["Official Website"]}]})
    nodes.append({"tag": "p", "children": ["Follow us: ", {"tag": "a", "attrs": {"href": "https://www.instagram.com/digital_nagari__software__ott/"}, "children": ["Instagram"]}]})
    
    data = {
        "access_token": TELEGRAPH_TOKEN,
        "title": title,
        "author_name": "Digital Nagari Network",
        "content": json.dumps(nodes),
        "return_content": False
    }

    try:
        response = requests.post(url, data=data, timeout=20)
        res = response.json()
        return res["result"]["url"] if res.get("ok") else None
    except:
        return None

def ping_index_now(article_url):
    """Pings IndexNow for instant discovery."""
    try:
        data = {
            "host": "telegra.ph",
            "key": "2d8f9a1b4e6c4d5a8b7c9d0e1f2a3b4c",
            "keyLocation": f"https://telegra.ph/indexnow-key.txt",
            "urlList": [article_url]
        }
        requests.post("https://api.indexnow.org/indexnow", json=data, timeout=10)
    except:
        pass

def main():
    if not GROQ_API_KEY or not TELEGRAPH_TOKEN:
        print("Missing API Keys.")
        return

    article = get_content()
    if article and 'title' in article:
        url = publish_to_telegraph(article['title'], article['paragraphs'])
        if url:
            ping_index_now(url)
            log_entry = f"[{datetime.now()}] {article['title']} -> {url}\n"
            with open(LOG_FILE, "a") as f:
                f.write(log_entry)
            print(f"Success: {url}")

if __name__ == "__main__":
    main()
