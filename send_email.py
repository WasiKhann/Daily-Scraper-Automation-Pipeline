import smtplib, ssl, os, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Read environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Load content
with open("notion.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Split by exact separator line: ".."
snippets = []
current_snippet = []

for line in lines:
    if line.strip() == "..":
        if current_snippet:
            snippets.append("".join(current_snippet).strip())
            current_snippet = []
    else:
        current_snippet.append(line)

# Add last snippet if file doesn't end with `..`
if current_snippet:
    snippets.append("".join(current_snippet).strip())

# Filter out empty results
snippets = [s for s in snippets if s.strip()]

# Debug print
print(f"🧪 Total snippets found: {len(snippets)}")

# Pick one snippet
chosen = random.choice(snippets)

# Email composition
msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = "🌙 Your Daily Islamic Reminder"
msg.attach(MIMEText(chosen, "plain"))

# Email sending
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

print("✅ Email sent successfully.")
print("--- Sent Snippet ---")
print(chosen)
