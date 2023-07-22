from flask import Flask, render_template, request
import re
import os
from flask_sqlalchemy import SQLAlchemy


def strongpassword(password):
    return ""


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.db")
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/")
def student():
    return render_template("base.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/sign", methods=["POST", "GET"])
def sign():
    if request.method == "POST":
        result = request.form

        username = result["Username"]
        password = result["Password"]

        newUser = User(username, password)
        db.session.add_all([newUser])
        db.session.commit()
        print("newUser.id", newUser.id)

        return render_template("base.html")


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        result = request.form

        username = result["Username"]
        password = result["Password"]
        registeredUser = User.query.filter(
            User.username == username and User.password == password
        )
        if registeredUser:
            return render_template("secretPage.html", result=result)

        return render_template("wrong.html")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
