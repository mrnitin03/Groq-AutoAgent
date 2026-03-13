import os
import json
import requests
from datetime import datetime

# Environment Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")

def generate_article():
    """Generates SEO content using Groq llama3-70b."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        "Write a professional news-style article about 'Digital Nagari' as a digital product platform. "
        "Include a title and 3-5 paragraphs. "
        "Output strictly in JSON format with keys: 'title' (string) and 'content' (list of strings for paragraphs)."
    )
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Groq API Error: {e}")
        return None

def publish_to_telegraph(json_data):
    """Converts text to Telegraph Node format and publishes."""
    try:
        data = json.loads(json_data)
        title = data.get("title", "Digital Nagari Daily Update")
        paragraphs = data.get("content", [])

        # Construct Telegraph Node structure (Required for API)
        telegraph_content = []
        for p in paragraphs:
            telegraph_content.append({"tag": "p", "children": [p]})

        url = "https://api.telegra.ph/createPage"
        payload = {
            "access_token": TELEGRAPH_TOKEN,
            "title": title,
            "author_name": "Digital Nagari Network",
            "content": json.dumps(telegraph_content),
            "return_content": False
        }

        r = requests.post(url, data=payload, timeout=20).json()
        if r.get("ok"):
            return r["result"]["url"]
        print(f"Telegraph Error: {r.get('error')}")
    except Exception as e:
        print(f"Publication Logic Error: {e}")
    return None

def index_now(article_url):
    """Sends IndexNow ping."""
    # Using a standard 32-char hex key for the ping structure
    data = {
        "host": "telegra.ph",
        "key": "4c3e8a2b1f0d4b5c8a9e7f6d5c4b3a21", 
        "keyLocation": "https://telegra.ph/4c3e8a2b1f0d4b5c8a9e7f6d5c4b3a21.txt",
        "urlList": [article_url]
    }
    try:
        requests.post("https://api.indexnow.org/indexnow", json=data, timeout=10)
    except:
        pass

def main():
    # Ensure verification file exists to prevent Git errors
    if not os.path.exists("verification_pack.txt"):
        with open("verification_pack.txt", "w") as f:
            f.write("DigitalNagari Auto-Agent Logs\n============================\n")

    if not GROQ_API_KEY or not TELEGRAPH_TOKEN:
        print("Error: Missing API Secrets")
        return

    print("Generating Article...")
    raw_content = generate_article()
    
    if raw_content:
        print("Publishing to Telegraph...")
        url = publish_to_telegraph(raw_content)
        
        if url:
            index_now(url)
            log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Success: {url}\n"
            with open("verification_pack.txt", "a") as f:
                f.write(log_entry)
            print(f"Process Complete: {url}")
        else:
            print("Failed to publish article.")
    else:
        print("Failed to generate article.")

if __name__ == "__main__":
    main()
