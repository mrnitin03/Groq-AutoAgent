import requests

def generate():
    url = "https://api.telegra.ph/createAccount"
    params = {"short_name": "DigitalNagari", "author_name": "Digital Nagari"}
    try:
        r = requests.get(url, params=params).json()
        if r.get("ok"):
            token = r["result"]["access_token"]
            with open("telegraph_token.txt", "w") as f:
                f.write(token)
            print(f"TELEGRAPH_TOKEN: {token}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate()
