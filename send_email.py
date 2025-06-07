import smtplib
import os
import random
import re
from email.mime.text import MIMEText

# Read Notion-scraped content
with open("notion.txt", "r", encoding="utf-8") as f:
    all_text = f.read()

# Normalize newlines
all_text = all_text.replace("\r\n", "\n")

# ✅ Split wherever 3+ newlines appear (Notion double blank lines = 3 \n)
snippets = re.split(r'\n{3,}', all_text)
snippets = [s.strip() for s in snippets if s.strip()]

# Pick a random snippet
print(f"\n🧪 Total snippets found: {len(snippets)}")
for i, s in enumerate(snippets, 1):
    print(f"\n--- Snippet {i} ---\n{s}\n")

chosen = random.choice(snippets)

# Setup email
sender = os.environ["EMAIL_USER"]
password = os.environ["EMAIL_PASS"]
receiver = os.environ["EMAIL_RECEIVER"]

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
    print("✅ Email sent successfully.")
    print(f"📤 Sent snippet:\n{chosen}")
except Exception as e:
    print(f"❌ Email failed to send: {e}")
