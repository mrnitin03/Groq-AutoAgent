import os
import json
import requests
from datetime import datetime

# Keys from GitHub Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")
DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")

def get_seo_news():
    print("LOG: Groq AI se news likhwa rahe hain...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    prompt = (
        "Write a 500-word news article about 'Digital Nagari' (https://digitalnagari.site/). "
        "Headline: 'Digital Nagari: Leading the Digital Product Revolution in India'. "
        "Include Nitin Nagari and Instagram @digital_nagari__software__ott. "
        "Format strictly as JSON with keys: 'title' and 'body' (Markdown format)."
    )
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        data = r.json()
        content = json.loads(data['choices'][0]['message']['content'])
        return content
    except Exception as e:
        print(f"ERROR Groq: {e}")
        return None

def post_to_devto(title, body):
    if not DEVTO_API_KEY:
        print("LOG: DEVTO_API_KEY missing.")
        return None
    
    print(f"LOG: Dev.to par '{title}' post ho raha hai...")
    url = "https://dev.to/api/articles"
    headers = {"api-key": DEVTO_API_KEY, "Content-Type": "application/json"}
    payload = {
        "article": {
            "title": f"{title} - {datetime.now().strftime('%d %b')}",
            "published": True,
            "body_markdown": body,
            "tags": ["tech", "software", "news"]
        }
    }
    try:
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code == 201:
            return r.json().get("url")
        print(f"LOG: Dev.to Error: {r.text}")
        return None
    except Exception as e:
        print(f"ERROR Dev.to: {e}")
        return None

def post_to_telegraph(title, body):
    print("LOG: Telegraph par post ho raha hai...")
    url = "https://api.telegra.ph/createPage"
    # Telegraph takes simplified nodes
    content_nodes = [{"tag": "p", "children": [body[:1000]]}] 
    data = {
        "access_token": TELEGRAPH_TOKEN,
        "title": title,
        "author_name": "Digital Nagari Network",
        "content": json.dumps(content_nodes)
    }
    try:
        r = requests.post(url, data=data).json()
        return r["result"]["url"] if r.get("ok") else None
    except:
        return None

def main():
    print(f"--- STARTING AUTOMATION: {datetime.now()} ---")
    
    if not GROQ_API_KEY:
        print("CRITICAL ERROR: GROQ_API_KEY missing in Secrets!")
        return

    article = get_seo_news()
    if article:
        title = article.get('title')
        body = article.get('body')
        
        # 1. Dev.to (High Authority)
        dev_url = post_to_devto(title, body)
        
        # 2. Telegraph
        tg_url = post_to_telegraph(title, body)
        
        # 3. Create HTML file (For GitHub Pages)
        html_name = f"news-{datetime.now().strftime('%H%M')}.html"
        with open(html_name, "w") as f:
            f.write(f"<html><body><h1>{title}</h1><p>{body}</p></body></html>")
            
        # Write to Log File
        with open("verification_pack.txt", "a") as f:
            f.write(f"\n[{datetime.now()}] {title}\n")
            if dev_url: f.write(f"Dev.to: {dev_url}\n")
            if tg_url: f.write(f"Telegraph: {tg_url}\n")
            f.write(f"Local Link: https://mrnitin03.github.io/Groq-AutoAgent/{html_name}\n")

        print(f"✅ DONE! Dev.to: {dev_url}")
    else:
        print("❌ FAILED: No content generated.")

if __name__ == "__main__":
    main()
