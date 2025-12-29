from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Wish route (frontend sends name)
@app.route("/wish", methods=["POST"])
def wish():
    name = request.json.get("name")

    # Save name to file
    with open("names.txt", "a") as f:
        f.write(name + "\n")

    return f"May this year bring success, happiness and peace ✨"

# Admin page to view all entered names
@app.route("/admin", methods=["GET"])
def admin():
    # Simple password protection
    password = request.args.get("password")
    if password != "newyear2025":  # change password if you want
        return "❌ Access denied. Please provide the correct password in the URL."

    try:
        with open("names.txt", "r") as f:
            names = f.read().splitlines()
    except FileNotFoundError:
        names = []

    # Simple HTML to display names
    html = "<h1>🎉 Entered Names 🎉</h1>"
    if names:
        html += "<ul>"
        for name in names:
            html += f"<li>{name}</li>"
        html += "</ul>"
    else:
        html += "<p>No names yet!</p>"

    return render_template_string(html)

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


