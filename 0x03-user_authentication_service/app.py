#!/usr/bin/env python3
"""Flask app module"""
from flask import (
    Flask,
    jsonify,
    request,
    abort,
    redirect,
    make_response
)
from auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """Route that returns a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Register a new user"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify(
            {"email": user.email, "message": "user created"}
        )
    except ValueError:
        return jsonify(
            {"message": "email already registered"}
        ), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Log in a user and creates a session"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email=email, password=password):
        abort(401, description="Invalid email or password")
    session_id = AUTH.create_session(email=email)
    response = make_response(
        jsonify({"email": email, "message": "logged in"}),
        200
    )
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Log out a user by destroying their session"""
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(
            403,
            description="Session ID is missing or invalid"
        )

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/", code=302)
    else:
        abort(
            403,
            description="Invalid session or user not found"
        )


@app.route("/profile", methods=["GET"])
def profile():
    """Fetches the user's profile information"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403, description="Session ID is missing or invalid")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify(
            {"email": user.email, "message": "logged in"}
        )
    else:
        abort(403, description="Invalid session or user not found")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
