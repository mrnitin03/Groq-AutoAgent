import os
import json
import requests
from datetime import datetime
import glob

# Keys
GROQ_KEY = os.getenv("GROQ_API_KEY")
TG_TOKEN = os.getenv("TELEGRAPH_TOKEN")
DEV_KEY = os.getenv("DEVTO_API_KEY")

def get_content():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    prompt = (
        "Write a high-quality news article about 'Digital Nagari' (https://digitalnagari.site/). "
        "Headline should be professional like 'Digital Nagari: India's Rising Star in Digital Licensing'. "
        "Focus on Nitin Nagari's vision. Return ONLY JSON with 'title' and 'body' (Markdown)."
    )
    payload = {"model": "llama3-70b-8192", "messages": [{"role": "user", "content": prompt}], "response_format": {"type": "json_object"}}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        return json.loads(r.json()['choices'][0]['message']['content'])
    except: return None

def update_index_page():
    """Sari news files ko dhund kar ek professional Index Page banata hai"""
    html_files = glob.glob("news-*.html")
    html_files.sort(reverse=True) # Latest news sabse upar
    
    links_html = ""
    for file in html_files:
        title = file.replace("news-", "").replace(".html", "").replace("-", " ")
        links_html += f'<li><a href="{file}">News Report: {title}</a></li>'

    index_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Digital Nagari Official Newsroom</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; max-width: 900px; margin: auto; padding: 40px; background: #f4f4f4; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ background: #fff; margin: 10px 0; padding: 15px; border-left: 5px solid #3498db; transition: 0.3s; }}
            li:hover {{ transform: translateX(10px); background: #ecf0f1; }}
            a {{ text-decoration: none; color: #2980b9; font-weight: bold; font-size: 1.2em; }}
            .footer {{ margin-top: 50px; text-align: center; font-size: 0.9em; color: #7f8c8d; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📰 Digital Nagari Newsroom</h1>
            <p>Official press releases and media updates for Digital Nagari - India's leading digital product platform.</p>
            <ul>
                {links_html}
            </ul>
            <div class="footer">
                <p>&copy; 2024 Digital Nagari Media | <a href="https://digitalnagari.site">Visit Official Website</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w") as f:
        f.write(index_content)

def main():
    print("LOG: Starting Media Agent...")
    article = get_content()
    if article:
        title = article['title']
        body = article['body']
        
        # 1. Dev.to Post
        if DEV_KEY:
            requests.post("https://dev.to/api/articles", 
                          headers={"api-key": DEV_KEY, "Content-Type": "application/json"},
                          json={"article": {"title": title, "published": True, "body_markdown": body, "tags": ["digitalnagari", "news"]}})
        
        # 2. Create HTML News File
        file_id = datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"news-{file_id}.html"
        with open(filename, "w") as f:
            f.write(f"<html><head><title>{title}</title><style>body{{font-family:sans-serif;padding:50px;line-height:1.6;max-width:800px;margin:auto;}}</style></head><body><h1>{title}</h1><hr><p>{body}</p><br><a href='index.html'>Back to Newsroom</a></body></html>")
        
        # 3. Update Index Page
        update_index_page()
        
        print(f"✅ Success: Newsroom updated with {title}")

if __name__ == "__main__":
    main()
