# main_program.py

import csv
import smtplib
from email.mime.text import MIMEText
import os

def read_email(file_path):
    try:
        with open(file_path, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            headers = ["almName", "almstatus", "time", "subject", "body","status","index"]
            return [dict(zip(headers, row)) for row in reader]
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found. Please make sure it exists.")
        return None

def read_recipients(file_path):
    try:
        with open(file_path, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            return [row[1] for row in reader if len(row) > 1]  # Extract email addresses
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found. Please make sure it exists.")
        return None

def read_smtp(file_path):
    try:
        with open(file_path, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            headers = ["server", "username", "password", "port"]
            return [dict(zip(headers, row)) for row in reader]
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found. Please make sure it exists.")
        return None

if __name__ == "__main__":
  smtp_data = read_smtp("./smtp.csv")
  recipients_data = read_recipients("./recipients.csv")
  email_data = read_email("./email.csv")
  if (smtp_data is not None) and (recipients_data is not None) and (email_data is not None):
    # SMTP Configuration
    server = smtp_data[0]['server']
    port = smtp_data[0]['port']
    username = smtp_data[0]['username']
    password = smtp_data[0]['password']

    # Create the email.
    recipients = []
    alarm_name = email_data[0]['almName']
    alarm_status = email_data[0]['almstatus']
    alarm_time = email_data[0]['time']
    alarm_body = email_data[0]['body']

    body = f"<html><head></head><body>{alarm_body} <p>Alarm: {alarm_name} </p><p>Alarm Time: {alarm_time}</p><p>Alarm Status: {alarm_status}</body></html>"
    for s in recipients_data:
      if s and s.strip():
        recipients.append(s)
    try:
      msg = MIMEText(body, 'html')
      msg['Subject'] = email_data[0]['subject']
      msg['From'] = username

      with smtplib.SMTP(server, port) as smtpserver:
        smtpserver.starttls()  # Enable TLS if needed
        smtpserver.login(username, password)
        smtpserver.sendmail(username, recipients, msg.as_string())
        print("Email sent successfully")
        if os.path.exists("email.csv"):
          os.remove("email.csv")
    except smtplib.SMTPException as e:
      print(f"Error sending email: {e}")
      print("SMTP Debugging Output:")
      print(server.get_debuglevel())  # Print debugging info

  else:
    print("Data is not correct")
