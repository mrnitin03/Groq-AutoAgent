import os
import json
import requests
from datetime import datetime

# API Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")
LOG_FILE = "verification_pack.txt"

def get_news_content():
    print("LOG: Starting Groq API Request...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    prompt = (
        "Write a 500-word professional news article about 'Digital Nagari' (https://digitalnagari.site/). "
        "Focus on: Best Deals on Software, AI Tools, and OTT subscriptions in India. "
        "Mention Nitin Nagari and Instagram @digital_nagari__software__ott. "
        "Return ONLY a JSON object with: 'title' and 'paragraphs' (list of strings)."
    )
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"LOG: Groq Status Code: {res.status_code}")
        if res.status_code != 200:
            print(f"LOG: Groq Error Body: {res.text}")
            return None
        
        data = res.json()
        return json.loads(data['choices'][0]['message']['content'])
    except Exception as e:
        print(f"LOG: Groq Exception: {str(e)}")
        return None

def publish_to_telegraph(title, paragraphs):
    print("LOG: Publishing to Telegraph...")
    url = "https://api.telegra.ph/createPage"
    
    # Building nodes with brand images
    nodes = [
        {"tag": "img", "attrs": {"src": "https://digitalnagari.site/wp-content/uploads/2023/11/cropped-logo-1.png"}},
        {"tag": "h3", "children": ["Digital Nagari Exclusive News"]}
    ]
    
    for p in paragraphs:
        nodes.append({"tag": "p", "children": [p]})
    
    nodes.append({"tag": "hr"})
    nodes.append({"tag": "p", "children": ["Visit: ", {"tag": "a", "attrs": {"href": "https://digitalnagari.site/"}, "children": ["digitalnagari.site"]}]})

    payload = {
        "access_token": TELEGRAPH_TOKEN,
        "title": title,
        "author_name": "Digital Nagari Media",
        "content": json.dumps(nodes)
    }

    try:
        r = requests.post(url, data=payload).json()
        if r.get("ok"):
            return r["result"]["url"]
        else:
            print(f"LOG: Telegraph API Error: {r.get('error')}")
            return None
    except Exception as e:
        print(f"LOG: Telegraph Exception: {str(e)}")
        return None

def main():
    if not GROQ_API_KEY or not TELEGRAPH_TOKEN:
        print("LOG: ERROR - Missing API Secrets in GitHub!")
        return

    article = get_news_content()
    if article and 'title' in article:
        link = publish_to_telegraph(article['title'], article['paragraphs'])
        if link:
            with open(LOG_FILE, "a") as f:
                f.write(f"[{datetime.now()}] {article['title']} | URL: {link}\n")
            print(f"LOG: SUCCESS! Created: {link}")
        else:
            print("LOG: ERROR - Failed to publish to Telegraph.")
    else:
        print("LOG: ERROR - Failed to get content from Groq.")

if __name__ == "__main__":
    main()
