Overview
This framework is designed to detect and exploit potential blind SQL injection vulnerabilities in web applications. It automates the process of testing various payloads to identify vulnerabilities and can upload a webshell if a vulnerability is found.

Features

Automated SQL Injection Testing: Uses a list of payloads to test for blind SQL injection vulnerabilities.

Logging and Reporting: Logs detailed information about each test, including status code, response time, content length, and a snippet of the response.

Webshell Upload: Attempts to upload a webshell if a vulnerability is detected, providing a pseudo shell for further exploitation.

Error Handling: Captures and logs errors that occur during testing.

Requirements

Python 3.11

requests library

Installation

Ensure you have Python 3.11 installed on your system.

Install the requests library:

pip install requests

Usage

Command Line Arguments

url: The vulnerable URL to test (e.g., https://example.com/vulnerable_uri).

payloads: File containing SQL injection payloads (default: payloads.txt).

--param: The parameter to test (default: ?id=2).

Running the Script

Create a file named payloads.txt and populate it with your SQL injection payloads.

Run the script with the required arguments:

python3 sqli.py <url> <payloads> --param <parameter>

Example

python3 sqli.py https://example.com/vulnerable_uri payloads.txt --param ?id=2
