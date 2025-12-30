from flask import Flask, render_template, request
from datetime import datetime
import random
import hashlib

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Wish route
@app.route("/wish", methods=["POST"])
def wish():
    name = request.json.get("name")

    # Save name with timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("names.txt", "a") as f:
        f.write(f"{name} | {now}\n")

    # Get quote
    quote = get_quote(name)
    return quote

# Admin page
@app.route("/admin", methods=["GET"])
def admin():
    password = request.args.get("password")
    if password != "html-x-python-2026ok":
        return "❌ Access denied."

    try:
        with open("names.txt", "r") as f:
            entries = f.read().splitlines()
    except FileNotFoundError:
        entries = []

    return render_template("admin.html", entries=entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

# ------------------- Quote Function -------------------
def get_quote(name):
    name_clean = name.lower().strip()
    name_hash = hashlib.sha256(name_clean.encode()).hexdigest()

    # 🔐 Hidden hashes for private names
    SECRET_HASHES = [
        "fe9e52d99d47fb6fc686df14e7b437d7a7b4215bc8555043335ec2ec2fdba629",  # likitha
        "97a993f4d571b66972a9a5b8660709e021ca03b725f222a83aedc570bc835769"   # likitha s / Likitha s
    ]

    # Private quote for special names
    if name_hash in SECRET_HASHES:
        return (
            "Some people enter our lives quietly,\n"
            "without needing to say much.\n\n"
            "Yet their presence somehow makes everything feel lighter.\n\n"
            "As this new year begins, may your days be calm,\n"
            "your moments comfortable, and your heart filled with simple joys.\n\n"
            "Happy New Year! 🎉\n"
            "May this year be bright, cheerful, and full of little surprises that make you smile."
        )

    # General quotes for everyone else
    general_quotes = [
        "May this new year gently remind you how strong you are,\n"
        "how far you’ve come, and how much more happiness\n"
        "you truly deserve.",

        "Let this year be softer on your heart,\n"
        "brighter in your dreams,\n"
        "and kinder to your soul.",

        "Some years change us loudly.\n"
        "Some change us quietly.\n"
        "May this one change you beautifully."
    ]

    return random.choice(general_quotes)
