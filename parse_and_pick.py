import random

# Read raw content
with open("notion.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Parse snippets using separator lines starting with `..`
snippets = []
current = []

for line in lines:
    if line.strip().startswith(".."):
        if current:
            snippets.append("".join(current).strip())
            current = []
    else:
        current.append(line)

# Add last snippet if any
if current:
    snippets.append("".join(current).strip())

# Filter out empty ones
snippets = [s for s in snippets if s.strip()]

print(f"🧪 Found {len(snippets)} valid snippets.\n")
chosen = random.choice(snippets)

print("🎯 Selected snippet:\n")
print(chosen)

# Save to file
with open("picked_snippet.txt", "w", encoding="utf-8") as f:
    f.write(chosen)
