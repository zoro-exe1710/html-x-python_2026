from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/wish", methods=["POST"])
def wish():
    name = request.json.get("name")

    # Save name to file
    with open("names.txt", "a") as f:
        f.write(name + "\n")

    return f"May this year bring success, happiness and peace ✨"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

