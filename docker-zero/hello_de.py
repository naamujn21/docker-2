import os

# Bahar se "USER_NAME" naam ka variable mangwao
user = os.getenv("USER_NAME", "Unknown User")

print(f"Hiii {user}! Processing your data...")

with open("output.txt", "a") as f: # 'a' matlab append (purane data ke niche likhna)
    f.write(f"\nTask done for: {user}")