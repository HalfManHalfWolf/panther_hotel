from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB = "hotel.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        checkin TEXT NOT NULL,
        checkout TEXT NOT NULL,
        room_type TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    if request.method == "POST":
        name = request.form["name"]
        checkin = request.form["checkin"]
        checkout = request.form["checkout"]
        room_type = request.form["room_type"]

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO reservations (name, checkin, checkout, room_type) VALUES (?, ?, ?, ?)",
                  (name, checkin, checkout, room_type))
        conn.commit()
        conn.close()

        return redirect(url_for("confirmation", name=name, checkin=checkin, checkout=checkout))
    return render_template("reservation.html")

@app.route("/confirmation")
def confirmation():
    name = request.args.get("name")
    checkin = request.args.get("checkin")
    checkout = request.args.get("checkout")
    return render_template("confirmation.html", name=name, checkin=checkin, checkout=checkout)

@app.route("/manager")
def manager():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name, checkin, checkout, room_type FROM reservations")
    rows = c.fetchall()
    conn.close()
    return render_template("reservation_list.html", reservations=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
