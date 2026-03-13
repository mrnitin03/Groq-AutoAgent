import requests
import json

def generate_telegraph_token():
    url = "https://api.telegra.ph/createAccount"
    params = {
        "short_name": "DigitalNagari",
        "author_name": "AI Agent"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("ok"):
            token = data["result"]["access_token"]
            with open("telegraph_token.txt", "w") as f:
                f.write(token)
            print(f"Token generated and saved to telegraph_token.txt: {token}")
        else:
            print(f"Error: {data.get('error')}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    generate_telegraph_token()