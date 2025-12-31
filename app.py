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
    SECRET_HASHES = [
        "fe9e52d99d47fb6fc686df14e7b437d7a7b4215bc8555043335ec2ec2fdba629", 
        "97a993f4d571b66972a9a5b8660709e021ca03b725f222a83aedc570bc835769",  
        "d9c1e9c9f06a2c6e3e7a0e6bff0d44c44c7b9c9b1bb3c0c7a4c5f9c0b3b0a2d4",
        "9c7bb45f9a44a2f6d7e7e2db9a39e4cf1d7c84a1e5b8a1c9e8c3b9a7d4f2e5a1",
        "f2c4a0c1a2a93e9a1a3a0a7c8b9e2e5c7d1b0a9f3c6e8d9b4a5c7e1f2d3b8",
        "9f2d8c4a7b3e6a5c1f0d9e8b2a4c6f7e3d1b5a0c9e8f4b6d7a2c3e1"
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
        "May this new year gently remind you how strong you truly are,\n"
        "not just in the big moments, but in all the quiet days you kept going.\n\n"
        "May it remind you of how far you’ve come,\n"
        "of the lessons you learned, the challenges you faced,\n"
        "and the courage you showed even when no one noticed.\n\n"
        "And above all, may this year bring you the kind of happiness\n"
        "that feels calm, genuine, and lasting —\n"
        "the kind you truly deserve.",


        "Let this year be softer on your heart,\n"
        "giving you space to breathe, heal, and feel at ease.\n\n"
        "May your dreams feel brighter and clearer,\n"
        "guiding you toward moments that truly matter to you.\n\n"
        "And may your soul be treated with kindness —\n"
        "through peaceful days, small joys, and quiet happiness\n"
        "that stays with you as the year goes on.",
        
        
        "Some years arrive with noise and rush,\n"
        "shaping us through moments we never forget.\n\n"
        "Others move softly, almost unnoticed,\n"
        "changing us in small, meaningful ways.\n\n"
        "May this year touch your life gently,\n"
        "guide you toward growth without pressure,\n"
        "and change you beautifully —\n"
        "in ways you’ll only realize when you look back."

    ]
    
    return random.choice(general_quotes)


# ------------------- Routes -------------------
# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Wish route
@app.route("/wish", methods=["POST"])
def wish():
    name = request.json.get("name")

    quote = get_quote(name)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("names.txt", "a", encoding="utf-8") as f:
        f.write(f"{name} | {quote.replace(chr(10), ' ')} | {now}\n")

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


# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


