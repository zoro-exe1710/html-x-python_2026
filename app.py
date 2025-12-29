from flask import Flask, render_template, request
from datetime import datetime
import random

app = Flask(__name__)

# List of long, festive quotes
quotes = [
    "✨ May this New Year bring you peace, joy, and success in every step you take. Let every day shine brighter than the last! ✨",
    "🎆 Wishing you a year filled with adventure, laughter, and dreams coming true. May happiness follow you everywhere! 🎆",
    "🌟 As the fireworks light up the sky, may your life be illuminated with love, health, and prosperity throughout the year! 🌟",
    "🎉 Cheers to a fresh start, new opportunities, and beautiful memories. May this year be your best chapter yet! 🎉",
    "💫 May your journey ahead be as colorful and magical as these fireworks. Wishing you endless joy and success! 💫"
]

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

    # Choose a random quote
    quote = random.choice(quotes)
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

    html = "<h1>🎉 Entered Names 🎉</h1><table border='1' cellpadding='10'>"
    html += "<tr><th>Name</th><th>Date & Time</th></tr>"
    if entries:
        for entry in entries:
            if "|" in entry:
                name, time = entry.split("|")
                html += f"<tr><td>{name.strip()}</td><td>{time.strip()}</td></tr>"
    else:
        html += "<tr><td colspan='2'>No names yet!</td></tr>"
    html += "</table>"

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
