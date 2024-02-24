# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
import subprocess

base_url = "http://192-46-239-94.ip.linodeusercontent.com:8000/api"
ntfy_url = "http://192-46-239-94.ip.linodeusercontent.com/restAPI"
username = 'dave'
password = 'MM+mVss1988gz'

sent_cves_file = 'sent_cves.txt'

def get_request(url):
    """Führt eine GET-Anfrage mit Basic Auth aus."""
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler bei der Anfrage zu {url}: {response.status_code}")
        return None

def process_cve_details(cve_id, report_id):
    """Ruft die Details für eine spezifische CVE-ID ab und verarbeitet sie."""
    cve_url = f"{base_url}/cve/{cve_id}"
    cve_details = get_request(cve_url)
    if cve_details:
        cvss = cve_details.get('cvss', {}).get('v3', 'Unbekannt')
        vendors_info = ", ".join([f"{vendor}: {', '.join(products)}" for vendor, products in cve_details.get('vendors', {}).items()])
        return f"Titel: {vendors_info}\nID: {report_id}\nCVE: {cve_id}\nScore: {cvss}\n"
    return None

def process_reports():
    """Ruft die Liste der Berichte ab und verarbeitet jeden Bericht, um CVE-Details zu sammeln."""
    reports_url = f"{base_url}/reports"
    reports = get_request(reports_url)
    all_notifications = []

    if reports:
        for report in reports:
            report_id = report.get('id')
            report_detail_url = f"{base_url}/reports/{report_id}"
            report_details = get_request(report_detail_url)

            for alert in report_details.get('alerts', []):
                cve_id = alert.get('cve')
                cvss = alert.get('cvss') 
                cve_notification = process_cve_details(cve_id, report_id)
                if cve_notification:
                    parts = cve_notification.split("\n")
                    if len(parts) >= 4:
                        title, _, _, score = parts[:4]
                        send_ntfy(title.split(":")[1].strip(), report_id, cve_id, score.split(":")[1].strip(), ntfy_url)

def send_ntfy(title, id, cve, score, ntfy_url, sent_cves_file='sent_cves.txt'):
    """Sendet die Nachricht an ntfy."""
    cve_details = (
        f"Titel: {title}\n"
        f"ID: {id}\n"
        f"CVE: {cve}\n"
        f"Score: {score}\n"
    )
    try:
        cve_details = cve_details.replace('\\n', '\n')
        
        cve_details = cve_details.strip(' "\'\n')
        
        try:
            open(sent_cves_file, 'r')
        except FileNotFoundError:
            open(sent_cves_file, 'w').close()

        with open(sent_cves_file, 'r') as file:
            sent_cves = [line.strip() for line in file.readlines()]
            if cve in sent_cves:
                print(f"CVE {cve} wurde bereits gesendet.")
                return

        cve_title = f"🚨🚨 CVE Alert: {cve} 🚨🚨\n"

        full_message = cve_title + cve_details

        curl_command = [
            'curl', '-d', f"'{full_message}'", 
            '-H', 'Content-Type: application/json',
            ntfy_url
        ]
        

        subprocess.run(curl_command, check=True)

        with open(sent_cves_file, 'a') as file:
            file.write(cve + '\n')
        
        print("Benachrichtigung erfolgreich gesendet.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Senden der Benachrichtigung: {e}")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")

if __name__ == "__main__":
    process_reports()
