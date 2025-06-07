import smtplib
import os
import random
from email.mime.text import MIMEText

# Load scraped content
with open("notion.txt", "r", encoding="utf-8") as f:
    all_text = f.read()

# 🔹 Split on custom delimiter: two periods
snippets = [s.strip() for s in all_text.split("..") if s.strip()]

# Randomly select one
chosen = random.choice(snippets)

# Email credentials from GitHub Secrets
sender = os.environ["EMAIL_USER"]
password = os.environ["EMAIL_PASS"]
receiver = os.environ["EMAIL_RECEIVER"]

# Create the email message
msg = MIMEText(chosen)
msg["Subject"] = "🌙 Your Daily Islamic Reminder"
msg["From"] = sender
msg["To"] = receiver

# Send the email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
    print("✅ Email sent.")
    print(f"📤 Sent snippet:\n{chosen}")
except Exception as e:
    print(f"❌ Email error: {e}")
