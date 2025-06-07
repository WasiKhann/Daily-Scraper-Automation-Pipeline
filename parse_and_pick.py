import random

# Read raw content
with open("notion.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Parse snippets using line == ".." as separator
snippets = []
current = []

for line in lines:
    if line.strip() == "..":
        if current:
            snippets.append("".join(current).strip())
            current = []
    else:
        current.append(line)

# Add the last one if file doesn't end with ".."
if current:
    snippets.append("".join(current).strip())

# Filter out empty ones
snippets = [s for s in snippets if s]

# Print how many and one random
print(f"🧪 Found {len(snippets)} valid snippets.\n")
chosen = random.choice(snippets)
print("🎯 Selected snippet:\n")
print(chosen)
