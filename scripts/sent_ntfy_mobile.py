from main_notification import *

base_ntfy_url = os.getenv('BASE_NTFY_URL')

def check_and_send_cve(cve_value_string, extracted_data_string, file_path="sent_cves.txt"):
    file_path = "sent_cves_mobile.txt"
    
    try:
        with open(file_path, 'r') as file:
            sent_cves = file.read().splitlines()
    except FileNotFoundError:
        sent_cves = []

    if cve_value_string not in sent_cves:
        message = (f"🚨CVE-Alarm🚨\n"
                   f"{cve_value_string}\n"
                   f"{extracted_data_string}")
        
        response = requests.post({base_ntfy_url},
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
