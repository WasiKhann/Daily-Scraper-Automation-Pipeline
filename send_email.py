import smtplib
import os
import random
from email.mime.text import MIMEText

# Load and split content
with open("notion.txt", "r", encoding="utf-8") as f:
    all_text = f.read()

# Split by double newlines = separate snippets
snippets = [s.strip() for s in all_text.split("\n\n") if s.strip()]
chosen = random.choice(snippets)

# Prepare email
sender = os.environ["EMAIL_USER"]
password = os.environ["EMAIL_PASS"]
receiver = os.environ["EMAIL_RECEIVER"]

msg = MIMEText(chosen)
msg["Subject"] = "🌙 Your Daily Islamic Reminder"
msg["From"] = sender
msg["To"] = receiver

# Send email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
    print("✅ Email sent.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
