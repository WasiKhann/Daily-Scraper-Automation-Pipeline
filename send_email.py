import smtplib, ssl, os, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get credentials and recipient info from environment
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Read and clean Notion content
with open("notion.txt", "r", encoding="utf-8") as f:
    raw_content = f.read()

# Normalize line endings
raw_content = raw_content.replace('\r\n', '\n').replace('\r', '\n')

# Split using clean separator (lines that contain only `..`)
lines = raw_content.split('\n')
snippets = []
current_snippet = []

for line in lines:
    if line.strip() == '..':
        if current_snippet:
            snippets.append('\n'.join(current_snippet).strip())
            current_snippet = []
    else:
        current_snippet.append(line)

# Add last snippet if file doesn't end with `..`
if current_snippet:
    snippets.append('\n'.join(current_snippet).strip())

# Filter non-empty snippets
snippets = [s for s in snippets if s.strip()]
print(f"✅ Total snippets found: {len(snippets)}")

# Choose one at random
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

# Confirm
print(f"📤 Email sent successfully!")
print(f"--- Sent snippet ---\n{chosen}")
