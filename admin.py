from flask import Flask, request, render_template, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "supersecurekey"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "passwort123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("admin_panel"))
        return "Login fehlgeschlagen"
    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    with open("kunden.json") as f:
        kunden = json.load(f)
    with open("termine.json") as f:
        termine = json.load(f)

    if request.method == "POST":
        if "new_plate" in request.form:
            plate = request.form["new_plate"].strip().upper()
            if plate and plate not in kunden:
                kunden[plate] = {"termin": None}
                with open("kunden.json", "w") as f:
                    json.dump(kunden, f)
        if "new_termin" in request.form:
            termin = request.form["new_termin"].strip()
            if termin and termin not in termine:
                termine.append(termin)
                with open("termine.json", "w") as f:
                    json.dump(termine, f)

    return render_template("admin.html", kunden=kunden, termine=termine)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
