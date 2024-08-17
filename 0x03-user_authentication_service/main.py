#!/usr/bin/env python3
"""Main module"""
import requests

BASE_URL = "http://localhost:5000"
USER_URL = f"{BASE_URL}/users"
SESSION_URL = f"{BASE_URL}/sessions"
PROFILE_URL = f"{BASE_URL}/profile"
RESET_PASSWORD_URL = f"{BASE_URL}/reset_password"


def register_user(email: str, password: str) -> None:
    """Test user registration"""
    response = requests.post(
        USER_URL,
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "message": "user created"
    }


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with incorrect password"""
    response = requests.post(
        SESSION_URL,
        data={"email": email, "password": password}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login and return session ID"""
    response = requests.post(
        SESSION_URL,
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "email" in response_json and "message" in response_json
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test profile access without login"""
    response = requests.get(PROFILE_URL)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test profile access with valid session ID"""
    response = requests.get(
        PROFILE_URL,
        cookies={"session_id": session_id}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "guillaume@holberton.io"


def log_out(session_id: str) -> None:
    """Test logout"""
    response = requests.delete(
        SESSION_URL,
        cookies={"session_id": session_id},
        allow_redirects=False
    )
    assert response.status_code == 302


def reset_password_token(email: str) -> str:
    """Test reset password token generation"""
    response = requests.post(
        RESET_PASSWORD_URL,
        data={"email": email}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert (
        "email" in response_json and
        "reset_token" in response_json
    )
    return response_json["reset_token"]


def update_password(
    email: str,
    reset_token: str,
    new_password: str
) -> None:
    """Test password update"""
    response = requests.put(
        RESET_PASSWORD_URL,
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "message": "Password updated"
    }


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
