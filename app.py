from flask import Flask, render_template, request
from datetime import datetime
import random
import hashlib

app = Flask(__name__)

# ------------------- Quote Function -------------------
def get_quote(name):
    name_clean = name.lower().strip()
    name_hash = hashlib.sha256(name_clean.encode()).hexdigest()

    # 🔐 Hidden hashes for private names
    SECRET_HASHES_LIKITHA = [
        "fe9e52d99d47fb6fc686df14e7b437d7a7b4215bc8555043335ec2ec2fdba629",  # likitha
        "97a993f4d571b66972a9a5b8660709e021ca03b725f222a83aedc570bc835769"   # likitha s
    ]
    SECRET_HASHES_LISHA = [
        "d2a1b8e7f0c3d6a9b4e5f1a7c0d8b3e2f6a9d4b7c1e3f5a6b0c2d8e1f9a3b7c4",  # lisha
        "e4c2f9a1b3d6c7e8a0b2d5f1c3e7a9b4d6f1c2b8e3a0d5f7c1b9e4a6d3f8b2c1"   # lisha s
    ]

    # Private quote for Likitha
    if name_hash in SECRET_HASHES_LIKITHA:
        return (
            "Some people enter our lives quietly,\n"
            "without needing to say much.\n\n"
            "Yet their presence somehow makes everything feel lighter.\n\n"
            "As this new year begins, may your days be calm,\n"
            "your moments comfortable, and your heart filled with simple joys.\n\n"
    
            "The new year is your canvas,\n"
            "paint it with your dreams, laughter, and little moments of magic.\n\n"
            "May each day bring a spark of joy,\n"
            "and may all your wishes feel closer than ever.\n\n"
            "Happy New Year! 🎉\n"
            "Here’s to a bright, cheerful, and unforgettable year ahead!"
            " Once Again Happy New Year!!! 🎉\n"
            "May this year be bright, cheerful, and full of little surprises that make you smile."
    
            
            
            )

    # General quotes for everyone else
    general_quotes = [
        "May this new year gently remind you how strong you truly are,\n"
        "not just in the big moments, but in all the quiet days you kept going.\n\n"
        "May it remind you of how far you’ve come,\n"
        "of the lessons you learned, the challenges you faced,\n"
        "and the courage you showed even when no one noticed.\n\n"
        "And above all, may this year bring you the kind of happiness\n"
        "that feels calm, genuine, and lasting —\n"
        "the kind you truly deserve.\n\n"
        "Happy New Year! 🎉\n"
        "May this year be bright, cheerful, and full of little surprises that make you smile.",

        "Let this year be softer on your heart,\n"
        "giving you space to breathe, heal, and feel at ease.\n\n"
        "May your dreams feel brighter and clearer,\n"
        "guiding you toward moments that truly matter to you.\n\n"
        "And may your soul be treated with kindness —\n"
        "through peaceful days, small joys, and quiet happiness\n"
        "that stays with you as the year goes on.\n\n"
        "Happy New Year! 🎉\n"
        "May this year be bright, cheerful, and full of little surprises that make you smile.",

        "Some years arrive with noise and rush,\n"
        "shaping us through moments we never forget.\n\n"
        "Others move softly, almost unnoticed,\n"
        "changing us in small, meaningful ways.\n\n"
        "May this year touch your life gently,\n"
        "guide you toward growth without pressure,\n"
        "and change you beautifully —\n"
        "in ways you’ll only realize when you look back.\n\n"
        "Happy New Year! 🎉\n"
        "May this year be bright, cheerful, and full of little surprises that make you smile."
    ]

    return random.choice(general_quotes)


# ------------------- Routes -------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/wish", methods=["POST"])
def wish():
    name = request.json.get("name")
    quote = get_quote(name)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Track who saw which quote
    with open("names.txt", "a", encoding="utf-8") as f:
        f.write(f"{name} | {quote.replace(chr(10), ' ')} | {now}\n")

    return quote


@app.route("/admin", methods=["GET"])
def admin():
    password = request.args.get("password")
    if password != "html-x-python-2026ok":
        return "❌ Access denied."

    try:
        with open("names.txt", "r", encoding="utf-8") as f:
            entries = f.read().splitlines()
    except FileNotFoundError:
        entries = []

    return render_template("admin.html", entries=entries)


# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
