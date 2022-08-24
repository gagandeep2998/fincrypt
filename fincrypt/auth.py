from flask import Blueprint, request, url_for, redirect, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        name = request.args.get("name")
        email = request.args.get("email")
        password = request.args.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify(
                Error="You are already registered with this email, login instead"
            ), 409

        hash_and_salt_password = generate_password_hash(
            password,
            method="pbkdf2:sha256",
            salt_length=8,
        )

        new_user = User(
            email=email,
            password=hash_and_salt_password,
            name=name
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(success="User registered successfully"), 201


@auth.route("/login", methods=["POST", "GET"])
def login():
    email = request.args.get("email")
    password = request.args.get("password")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(
            Error="User not found, try again"
        ), 404

    hash_password = user.password
    if check_password_hash(hash_password, password):
        login_user(user)
        return jsonify(Success="User loggedIn Successfully"), 200
    else:
        return jsonify(Error="Password doesn't match, try again"), 401


@auth.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify(Success="User logged out Successfully")


