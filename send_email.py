import smtplib, ssl, os, random, requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Settings ---
# Adjustable: How many snippets you want in the email
NUM_SNIPPETS = 5  # Change this to 1, 2, 3...

# --- Load Credentials ---
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Snippet Parsing ---
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

# --- Select and Prepare Content ---
# Choose random N snippets (limit to available number)
selected_snippets = random.sample(snippets, min(NUM_SNIPPETS, len(snippets)))

# Join them for the email body
email_body = "\n\n---\nIn other news...\n\n".join(selected_snippets)

# --- Send Email ---
if EMAIL_USER and EMAIL_PASS and EMAIL_RECEIVER:
    print("\n📬 Preparing to send email...")
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "🌙 Your Daily Islamic Reminder"
    msg.attach(MIMEText(email_body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
        print("✅ Email sent successfully.")
        print("📤 Sent content:\n")
        print(email_body)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
else:
    print("⚠️ Email credentials not found. Skipping email.")

# --- Send Telegram Message ---
if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
    print("\n✈️ Preparing to send Telegram message...")
    # We'll just send the first snippet to Telegram for brevity
    telegram_message = selected_snippets[0]
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": telegram_message,
        "parse_mode": "Markdown"  # Or "HTML" if you prefer
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("✅ Telegram message sent successfully.")
            print("📤 Sent content:\n")
            print(telegram_message)
        else:
            print(f"❌ Failed to send Telegram message. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")
else:
    print("⚠️ Telegram credentials not found. Skipping Telegram message.")
