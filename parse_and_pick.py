import random
import re

# Read entire file as one string
with open("notion.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Normalize line endings
content = content.replace("\r\n", "\n").replace("\r", "\n")

# Remove header/footer markers if present
content = re.sub(r"-------- NOTION\.TXT START --------", "", content)
content = re.sub(r"-------- NOTION\.TXT END ----------", "", content)

# Split content using regex that finds any line starting with `..`
snippets = re.split(r"\n\s*\.\.\s*\n", content)

# Clean and filter out empty ones
snippets = [s.strip() for s in snippets if s.strip()]

# Debug: show total and pick one
print(f"🧪 Found {len(snippets)} valid snippets.\n")

if not snippets:
    raise ValueError("❌ No valid snippets found. Check your `..` separator format.")

chosen = random.choice(snippets)

print("🎯 Selected snippet:\n")
print(chosen)

# Save to picked_snippet.txt
with open("picked_snippet.txt", "w", encoding="utf-8") as f:
    f.write(chosen)
