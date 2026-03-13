import requests

def create_telegraph_account():
    url = "https://api.telegra.ph/createAccount"
    params = {
        "short_name": "DigitalNagari",
        "author_name": "Digital Nagari Bot"
    }
    try:
        response = requests.get(url, params=params).json()
        if response.get("ok"):
            token = response["result"]["access_token"]
            with open("telegraph_token.txt", "w") as f:
                f.write(token)
            print("Successfully generated TELEGRAPH_TOKEN")
            print(f"Token: {token}")
            print("Save this token in your GitHub Secrets as: TELEGRAPH_TOKEN")
        else:
            print(f"Error: {response.get('error')}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    create_telegraph_account()
