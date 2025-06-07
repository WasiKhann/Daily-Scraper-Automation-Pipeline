import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load email credentials
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Load chosen snippet
with open("picked_snippet.txt", "r", encoding="utf-8") as f:
    chosen = f.read().strip()

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

print("✅ Email sent successfully.")
print("--- Sent Snippet ---")
print(chosen)
