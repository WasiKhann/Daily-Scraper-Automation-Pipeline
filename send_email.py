import smtplib
import os
import random
import re
from email.mime.text import MIMEText

# Read Notion content
with open("notion.txt", "r", encoding="utf-8") as f:
    all_text = f.read()

# Normalize newlines
all_text = all_text.replace("\r\n", "\n")

# ✅ Flexible split: 2 or more blank lines (any number of \n)
snippets = re.split(r'(?:\n\s*){2,}', all_text)
snippets = [s.strip() for s in snippets if s.strip()]

# Pick one
chosen = random.choice(snippets)

# Email setup
sender = os.environ["EMAIL_USER"]
password = os.environ["EMAIL_PASS"]
receiver = os.environ["EMAIL_RECEIVER"]

msg = MIMEText(chosen)
msg["Subject"] = "🌙 Your Daily Islamic Reminder"
msg["From"] = sender
msg["To"] = receiver

# Send it
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
    print("✅ Email sent.")
    print(f"📤 Snippet sent:\n{chosen}")
except Exception as e:
    print(f"❌ Email error: {e}")
