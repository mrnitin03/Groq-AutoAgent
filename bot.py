import os
import json
import requests
from datetime import datetime

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")

# Aapki Photo ka URL (Direct link)
MY_PHOTO_URL = "https://digitalnagari.site/wp-content/uploads/2024/logo.png" 

def get_news_content():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # AI ko "Journalist" banane ka prompt
    prompt = (
        "Write a formal news report about the rise of 'Digital Nagari' in the Indian Digital Market. "
        "Headline should be catchy like 'Digital Nagari Revolutionizes Software Licensing in India'. "
        "Mention the founder 'Nitin Nagari' and the website https://digitalnagari.site/. "
        "The tone must be journalistic, as if written by a tech news portal. "
        "Strictly return as JSON with keys: 'title' and 'paragraphs' (list of 5 strings)."
    )
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        return json.loads(response.json()['choices'][0]['message']['content'])
    except:
        return None

def publish_to_telegraph(title, paragraphs):
    url = "https://api.telegra.ph/createPage"
    
    # Telegraph Nodes build karna (With Image)
    nodes = []
    
    # 1. Pehle aapki Photo add karein
    nodes.append({"tag": "figure", "children": [{"tag": "img", "attrs": {"src": MY_PHOTO_URL}}]})
    
    # 2. Articles ke paragraphs add karein
    for p in paragraphs:
        nodes.append({"tag": "p", "children": [p]})
    
    # 3. Footer with Official Links
    nodes.append({"tag": "hr"})
    nodes.append({"tag": "p", "children": ["Source: ", {"tag": "a", "attrs": {"href": "https://digitalnagari.site/"}, "children": ["Digital Nagari Official Portal"]}]})

    data = {
        "access_token": TELEGRAPH_TOKEN,
        "title": title,
        "author_name": "Tech News Network",
        "content": json.dumps(nodes)
    }

    try:
        r = requests.post(url, data=data).json()
        return r["result"]["url"] if r.get("ok") else None
    except:
        return None

def main():
    print("Generating Professional News Article...")
    article = get_news_content()
    if article:
        link = publish_to_telegraph(article['title'], article['paragraphs'])
        if link:
            with open("verification_pack.txt", "a") as f:
                f.write(f"{datetime.now()} | NEWS LINK: {link}\n")
            print(f"Article Live: {link}")

if __name__ == "__main__":
    main()
