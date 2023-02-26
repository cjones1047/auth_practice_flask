from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
file_path = os.path.abspath(os.getcwd())+"/users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.form:
        # create Python dictionary from form data
        user_dict = dict(request.form)
        # remove keys for columns that do not exist in database:
        filtered_user_dict = {key: user_dict[key] for key in user_dict if key in dir(User)}
        # noinspection PyArgumentList
        created_user = User(**filtered_user_dict)
        db.session.add(created_user)
        db.session.commit()
        return render_template("secrets.html", user=created_user)

    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory("static",
                               "files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
