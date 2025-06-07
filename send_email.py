import smtplib, ssl, os, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Read and split Notion content
with open("notion.txt", "r", encoding="utf-8") as f:
    raw = f.read()
    # Split using the ".." separator with line breaks normalized
    blocks = [block.strip() for block in raw.split("..") if block.strip()]

# Pick one snippet randomly
snippet = random.choice(blocks)

# Compose the email
msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = "🌙 Your Daily Islamic Reminder"

msg.attach(MIMEText(snippet, "plain"))

# Send the email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

# Log
print(f"🧪 Total snippets found: {len(blocks)}")
print(f"📤 Sent snippet:\n{snippet}")
