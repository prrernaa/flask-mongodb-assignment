from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json

app = Flask(__name__)

# --------------------------
# MongoDB Atlas Connection
# --------------------------
client = MongoClient("YOUR_MONGODB_ATLAS_CONNECTION_STRING")
db = client["assignment_db"]
collection = db["users"]

# --------------------------
# API Route - Read from file
# --------------------------
@app.route("/api", methods=["GET"])
def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)

# --------------------------
# Form Page
# --------------------------
@app.route("/")
def form():
    return render_template("form.html")

# --------------------------
# Form Submission
# --------------------------
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form["name"]
        email = request.form["email"]

        if not name or not email:
            raise ValueError("All fields are required")

        collection.insert_one({
            "name": name,
            "email": email
        })

        return redirect(url_for("success"))

    except Exception as e:
        return render_template("form.html", error=str(e))

# --------------------------
# Success Page
# --------------------------
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)


# ─── Part 3: To-Do route ─────────────────────────────────────────────────────
todo_collection = db["todos"]

@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo():
    item_name        = request.form.get("itemName", "").strip()
    item_description = request.form.get("itemDescription", "").strip()

    if not item_name or not item_description:
        return render_template("todo.html", error="All fields are required.")

    try:
        todo_collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })
        return render_template("todo.html", success="To-Do item added successfully!")
    except PyMongoError as e:
        return render_template("todo.html", error=f"Database error: {str(e)}")
