from flask import Flask, render_template, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Wish route (frontend sends name)
@app.route("/wish", methods=["POST"])
def wish():
    name = request.json.get("name")

    # Save name with date & time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("names.txt", "a") as f:
        f.write(f"{name} | {now}\n")

    return f"May this year bring success, happiness and peace ✨"

# Admin page to view all entered names with date & time
@app.route("/admin", methods=["GET"])
def admin():
    # Simple password protection
    password = request.args.get("password")
    if password != "html-x-python-2026ok":  # admin password
        return "❌ Access denied. Provide the correct password in the URL."

    try:
        with open("names.txt", "r") as f:
            entries = f.read().splitlines()
    except FileNotFoundError:
        entries = []

    # Build festive HTML page
    html = """
    <html>
    <head>
        <title>🎆 Entered Names 🎆</title>
        <style>
            body {
                background: radial-gradient(circle, #ff9a9e, #fad0c4, #fad0c4, #fbc2eb);
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #fff;
                text-shadow: 2px 2px 5px #000;
                font-size: 3em;
                animation: glow 1.5s infinite alternate;
            }
            table {
                margin: 0 auto;
                border-collapse: collapse;
                width: 70%;
                background: rgba(255,255,255,0.8);
                border-radius: 10px;
                overflow: hidden;
            }
            th, td {
                padding: 15px;
                font-size: 1.2em;
            }
            th {
                background: linear-gradient(45deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff);
                background-size: 400% 400%;
                animation: rainbow 10s linear infinite;
                color: #000;
            }
            tr:nth-child(even) {background-color: rgba(255,255,255,0.6);}
            @keyframes rainbow {
                0%{background-position:0% 50%}
                50%{background-position:100% 50%}
                100%{background-position:0% 50%}
            }
            @keyframes glow {
                from {text-shadow: 0 0 10px #fff, 0 0 20px #ff0;}
                to {text-shadow: 0 0 20px #fff, 0 0 30px #f0f;}
            }
        </style>
    </head>
    <body>
        <h1>🎉 Entered Names 🎉</h1>
        <table border="1">
        <tr><th>Name</th><th>Date & Time</th></tr>
    """

    if entries:
        for entry in entries:
            if "|" in entry:
                name, time = entry.split("|")
                html += f"<tr><td>{name.strip()}</td><td>{time.strip()}</td></tr>"
    else:
        html += "<tr><td colspan='2'>No names yet!</td></tr>"

    html += "</table></body></html>"

    return render_template_string(html)

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



