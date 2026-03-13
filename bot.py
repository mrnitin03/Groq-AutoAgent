import os
import json
import requests
from datetime import datetime

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")
MODEL = "llama3-70b-8192"

def get_seo_content():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    prompt = (
        "Write a high-quality SEO article about 'The Future of AI Automation in 2024'. "
        "Format strictly as JSON: {'title': '...', 'paragraphs': ['...', '...']}"
    )
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return json.loads(response.json()['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Groq Error: {e}")
        return None

def publish_to_telegraph(title, paragraphs):
    url = "https://api.telegra.ph/createPage"
    content = [{"tag": "p", "children": [p]} for p in paragraphs]
    payload = {
        "access_token": TELEGRAPH_TOKEN,
        "title": title,
        "author_name": "DigitalNagari AI",
        "content": json.dumps(content)
    }
    try:
        response = requests.post(url, data=payload, timeout=20)
        res_data = response.json()
        return res_data.get("result", {}).get("url") if res_data.get("ok") else None
    except Exception as e:
        print(f"Telegraph Error: {e}")
        return None

def main():
    if not GROQ_API_KEY or not TELEGRAPH_TOKEN:
        return

    article = get_seo_content()
    if article and 'title' in article:
        url = publish_to_telegraph(article['title'], article['paragraphs'])
        if url:
            with open("verification_pack.txt", "a") as f:
                f.write(f"[{datetime.now()}] {article['title']} - {url}\n")
            print(f"Published: {url}")

if __name__ == "__main__":
    main()
