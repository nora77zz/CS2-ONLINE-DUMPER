import os
import time
import subprocess
import json
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()




API_URL = os.getenv("API_URL", "http://localhost:8001")
UPLOAD_ENDPOINT = f"{API_URL}/upload"
MASTER_KEY = os.getenv("MASTER_KEY")
if not MASTER_KEY:
    print("[!] MASTER_KEY environment variable is not set")
    exit(1)
DUMPER_EXE = "cs2-dumper.exe"
OUTPUT_DIR = "output"


def calculate_hash(content):
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()

def run_dumper():
    if not os.path.exists(DUMPER_EXE):
        print(f"[!] {DUMPER_EXE} not found. Make sure it is in the same directory.")
        return False

    print(f"[*] Running {DUMPER_EXE}...")
    try:

        subprocess.run([DUMPER_EXE], check=True)
        print("[+] Dumper finished successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running dumper: {e}")
        return False

def upload_files():
    output_path = Path(OUTPUT_DIR)
    if not output_path.exists():
        print(f"[!] Output directory '{OUTPUT_DIR}' not found.")
        return

    json_files = list(output_path.glob("*.json"))
    if not json_files:
        print("[-] No JSON files found to upload.")
        return

    print(f"[*] Found {len(json_files)} files. Starting upload...")

    headers = {
        "x-api-key": MASTER_KEY,
        "Content-Type": "application/json"
    }

    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)

            file_hash = calculate_hash(content)
            payload = {
                "filename": file_path.name,
                "content": content,
                "hash": file_hash
            }

            response = requests.post(UPLOAD_ENDPOINT, json=payload, headers=headers)
            
            if response.status_code == 201:
                print(f"[+] Uploaded: {file_path.name}")
            else:
                print(f"[!] Failed to upload {file_path.name}: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"[!] Error processing {file_path.name}: {e}")

def main():
    print("=== CS2-Central Local Worker ===")
    

    if run_dumper():

        upload_files()
    else:
        print("[!] Skipping upload due to dumper failure.")

    print("=== Done ===")

if __name__ == "__main__":
    main()
