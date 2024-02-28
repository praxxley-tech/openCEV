import smtplib
from main_notification import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def read_sent_cves(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def append_sent_cve(file_path, cve):
    with open(file_path, 'a') as file:
        file.write(cve + '\n')

def send_email_via_smtp(subject, body, to_email, smtp_info, cve_value_string, extracted_data_string):
    file_path = smtp_info.get("file_path", "sent_cves.txt")
    sent_cves = read_sent_cves(file_path)

    if cve_value_string.split(', ')[0] not in sent_cves:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = smtp_info['login']
        message["To"] = to_email

        body_with_data = f"{body} {cve_value_string}\n\n{extracted_data_string}"
        part1 = MIMEText(body_with_data, "plain")
        part2 = MIMEText(f"<html><body><p>{body_with_data}</p></body></html>", "html")

        message.attach(part1)
        message.attach(part2)

        try:
            with smtplib.SMTP(smtp_info['smtp_server'], smtp_info['port']) as server:
                server.starttls()
                server.login(smtp_info['login'], smtp_info['password'])
                server.sendmail(smtp_info['login'], to_email, message.as_string())
                for cve in cve_value_string.split(', '):
                    append_sent_cve(file_path, cve)
                print("Email erfolgreich gesendet!")
        except Exception as e:
            print(f"Fehler beim Senden der E-Mail: {e}")

subject = "🚨CVE-Alarm🚨"
body = ""
to_email = "d.rennhard@gmail.com"

send_email_via_smtp(subject, body, to_email, smtp_info, cve_value_string, extracted_data_string)