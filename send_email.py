import smtplib
import os
from email.mime.text import MIMEText

with open("notion.txt", "r", encoding="utf-8") as f:
    body = f.read()

sender = os.environ["EMAIL_USER"]
password = os.environ["EMAIL_PASS"]
receiver = os.environ["EMAIL_RECEIVER"]

msg = MIMEText(body)
msg["Subject"] = "🌙 Daily Islamic Reminder from Notion"
msg["From"] = sender
msg["To"] = receiver

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
    print("✅ Email sent.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
