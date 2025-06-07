import smtplib, ssl, os, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 👇 Adjustable: How many snippets you want in the email
NUM_SNIPPETS = 3  # Change this to 1, 2, 3...

# Load email credentials from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Read the entire content of notion.txt
with open("notion.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Normalize line endings
content = content.replace("\r\n", "\n").replace("\r", "\n")
lines = content.split("\n")
snippets = []
current = []

# Split by lines that equal ".."
for line in lines:
    if line.strip() == "..":
        if current:
            snippet = "\n".join(current).strip()
            if snippet:
                snippets.append(snippet)
            current = []
    else:
        current.append(line)
if current:
    snippet = "\n".join(current).strip()
    if snippet:
        snippets.append(snippet)

if not snippets:
    raise Exception("❌ No snippets found. Check that notion.txt contains separator lines with '..'.")

print(f"🧪 Found {len(snippets)} valid snippet(s).")

# Choose random N snippets (limit to available number)
selected = random.sample(snippets, min(NUM_SNIPPETS, len(snippets)))

# Join them with separator
joined = "\n\n---\nIn other news...\n\n".join(selected)

# Compose the email
msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = "🌙 Your Daily Islamic Reminder"
msg.attach(MIMEText(joined, "plain"))

# Send the email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

print("✅ Email sent successfully.")
print("📤 Sent content:\n")
print(joined)
