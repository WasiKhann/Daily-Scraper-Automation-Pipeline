import smtplib, ssl, os, random, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Read Notion content
with open("notion.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# Clean header garbage (title, duplication, etc.)
raw = re.sub(r"(?i)(most imp Notion page[\s\S]*?Get Notion free[\s\S]*?jannah IA)", "", raw).strip()

# Split using '..' as separator (with optional newlines or spaces)
snippets = re.split(r'\n?\s*\.\.\s*\n?', raw)
snippets = [s.strip() for s in snippets if s.strip()]

# Pick one at random
chosen = random.choice(snippets)

# Compose email
msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = "🌙 Your Daily Islamic Reminder"

msg.attach(MIMEText(chosen, "plain"))

# Send
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

# Log output
print(f"✅ Snippets found: {len(snippets)}")
print(f"📤 Sent:\n{chosen}")
