import requests

def generate_telegraph_token():
    url = "https://api.telegra.ph/createAccount"
    params = {"short_name": "DigitalNagari", "author_name": "AI Agent"}
    try:
        data = requests.get(url, params=params).json()
        if data.get("ok"):
            token = data["result"]["access_token"]
            with open("telegraph_token.txt", "w") as f:
                f.write(token)
            print(f"Token: {token}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_telegraph_token()
