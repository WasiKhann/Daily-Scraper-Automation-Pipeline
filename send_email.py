import smtplib, ssl, os, random, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# 1. Load raw content from Notion
with open("notion.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# 2. Remove repeated headers or placeholder lines
raw = re.sub(
    r"(?i)(Most imp Notion page[\s\S]*?Get Notion free[\s\S]*?jannah IA)",
    "",
    raw
).strip()

# Optional: remove any trailing lone `..`
raw = re.sub(r'\n*\.\.\s*$', '', raw).strip()

# 3. Split using ".." (flexible regex)
snippets = re.split(r'\n?\s*\.\.\s*\n?', raw)
snippets = [s.strip() for s in snippets if s.strip()]

# 4. Select one snippet
selected = random.choice(snippets)

# 5. Compose email
msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = "🌙 Your Daily Islamic Reminder"
msg.attach(MIMEText(selected, "plain"))

# 6. Send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

# 7. Log for debug
print(f"🧪 Total snippets found: {len(snippets)}")
print(f"✅ Email sent successfully.\n📤 Sent snippet:\n{selected}")
