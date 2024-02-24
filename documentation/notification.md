# CVE Alert System Documentation
This document provides a comprehensive guide to the CVE Alert System. The system is designed to fetch and process reports of Common Vulnerabilities and Exposures (CVEs) and send notifications for each report.

**System Requirments**

 - Python 3.x
 - 'requests' libary
 - Acces to a command-line interface for executing 'curl' commands

**Installation**

 1. Ensure Python 3.x is installed on your system.
 2. Install the 'requests' libary using pip:
 3. `pip install requests`
 4. Verify that 'curl' is available in your system's command-line interface.

**Configuration**

 - Base URL: The base URL for the API from wich CVE reports are fetched.
 - Notification URL: The URL to which notifications are sent.
 - Credentials: Username and password for basic authentication.

**Usage**
**Import Statements**

    import requests
    from requests.auth import HTTPBasicAuth
    import subprocess
**Configuration Variables**

    base_url = "http://examples:8000/api"
    ntfy_url = "http://examples/channel"
    username = <username>
    password = <password>

Replace server-ip, username, and password with your actual server IP, username and password.

**Functions**

`get_request(url)`

Performs a GET request with Basic Authentication.

   `process_cve_details(cve_id)`
   
Fetches and processes details for a specific CVE ID.

   `process_reports()`
   
Fetches the list of reports and processes each report to collect CVE details.

    `send_ntfy(title, id, cve, score, summary, ntfy_url, sent_cves_file='sent_cves.txt')`

Sends a notification message.

 -   `title`: The title of the notification.
 -   `id`: The ID of the report.
 -   `cve`: The CVE ID.
 -   `score`: The CVSS score of the CVE.
 -   `summary`: A summary of the CVE.
 -   `ntfy_url`: The URL to which the notification is sent.
 -   `sent_cves_file`: The file to track sent CVEs. Defaults to `sent_cves.txt`

**Main Exectuion**
The script's main execution flow starts by calling the `process_reports()` function.

** Troubleshooting**

 - Ensure all required libraries are installed and up-to-date.
-   Verify that the server IP, username, and password are correctly configured.
-   Check network connectivity to the base and notification URLs.

