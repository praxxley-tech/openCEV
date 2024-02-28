import json
import os
import subprocess
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

username = os.getenv('API_USERNAME')
password = os.getenv('API_PASSWORD')
base_url = "https://opencve.secopsitpoint.ch/api/reports"

def get_report_ids():
    response = requests.get(f"{base_url}",auth=HTTPBasicAuth(username, password))
    if response.ok:
        return response.json()
    return []

def get_detailed_reports():
    report_ids = get_report_ids()
    detailed_reports = []
    for report in report_ids:
        report_id = report['id']
        detailed_report_url = f"{base_url}/{report_id}"
        response = requests.get(detailed_report_url, auth=HTTPBasicAuth(username, password))
        report_details = response.json()
        detailed_reports.append(report_details) 
    return detailed_reports

result = get_detailed_reports()

def extract_key_values(results, keys):
    def get_value_by_path(dict_obj, path):
        parts = path.split('.')
        for part in parts[:-1]: 
            if isinstance(dict_obj, dict) and part in dict_obj:
                dict_obj = dict_obj[part]
            elif isinstance(dict_obj, list):
                return [get_value_by_path(elem, '.'.join(parts[parts.index(part):])) for elem in dict_obj if isinstance(elem, dict)]
            else:
                return None
        if isinstance(dict_obj, dict):
            return dict_obj.get(parts[-1])
        return None

    extracted_values = {key: [] for key in keys}
    for result in results:
        for key in keys:
            value = get_value_by_path(result, key)
            if value is not None:
                if isinstance(value, list): 
                    extracted_values[key].extend(value)
                else:
                    extracted_values[key].append(value)
    return extracted_values

def extract_cve_values(data):
    cve_values = []
    for item in data:
        if 'alerts' in item and isinstance(item['alerts'], list):
            for alert in item['alerts']:
                if 'cve' in alert:
                    cve_values.append(alert['cve'])
    return cve_values

def format_extracted_data(extracted_data):
    formatted_data = []
    for key in extracted_data:
        values = extracted_data[key]
        if isinstance(values[0], list):
            values = [', '.join(value) for value in values]
        formatted_data.append(f"{key}: {'; '.join(values)}")
    return '\n'.join(formatted_data)

cve_values = extract_cve_values(result)
cve_value_string = ', '.join(cve_values)
keys_to_extract = ["id", "details"]
extracted_data = extract_key_values(result, keys_to_extract)
extracted_data_string = format_extracted_data(extracted_data)

print("CVE:", cve_value_string)
print(extracted_data_string)


Message = (f"{cve_value_string}\n"
           f"{extracted_data_string}")

def check_and_send_cve(cve_value_string, extracted_data_string):
    file_path = "sent_cves.txt"
    
    try:
        with open(file_path, 'r') as file:
            sent_cves = file.read().splitlines()
    except FileNotFoundError:
        sent_cves = []

    if cve_value_string not in sent_cves:
        message = (f"🚨CVE-Alarm🚨\n"
                   f"{cve_value_string}\n"
                   f"{extracted_data_string}")
        
        response = requests.post("https://ntfy.secopsitpoint.ch/Daily_Updates",
                                 data=message.encode(encoding='utf-8'))
        
        if response.ok:
            print(f"Nachricht erfolgreich gesendet: {cve_value_string}")
            with open(file_path, 'a') as file:
                file.write(f"{cve_value_string}\n")
        else:
            print(f"Fehler beim Senden der Nachricht: {response.text}")
    else:
        print(f"CVE {cve_value_string} wurde bereits gesendet.")

check_and_send_cve(cve_value_string, extracted_data_string)
