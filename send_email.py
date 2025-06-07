import smtplib, ssl, os, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load credentials
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Read content
with open("notion.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Split into snippets using 2 or more newlines (paragraphs)
snippets = [s.strip() for s in content.split('\n\n') if s.strip()]

# Choose a random one
if not snippets:
    raise Exception("❌ No snippets found. Check notion.txt formatting.")
chosen = random.choice(snippets)

# Compose email
msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = "🌙 Your Daily Islamic Reminder"
msg.attach(MIMEText(chosen, "plain"))

# Send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

print("✅ Email sent.")
print("--- Sent Snippet ---\n", chosen)
