import pytest

name = "demo"
email = "demo@email.com"
password = "12345678"
unregistered_email = "demo2@gmail.com"
wrong_password = "wrong password"


@pytest.mark.order(1)
def test_user_registration(client):
    """Given the new user details
    checking if the new user could register or not
    """
    res = client.post(f"/register?name={name}&email={email}&password={password}")
    assert res.status_code == 201
    assert b'User registered successfully' in res.data


@pytest.mark.order(2)
def test_user_already_register(client):
    """Given the user details
    checking if the already registered user could register again
    """
    res = client.post(f"/register?name={name}&email={email}&password={password}")
    assert res.status_code == 409
    assert b'You are already registered with this email, login instead' in res.data


@pytest.mark.order(3)
def test_login_user(client):
    """Given the user credentials
    checking if the user could log in with correct credentials
    """
    res = client.post(f"/login?email={email}&password={password}")
    assert res.status_code == 200
    assert b'User loggedIn Successfully' in res.data


@pytest.mark.order(4)
def test_unregister_user_login(client):
    """Given the user credentials
    checking if the unregistered user could log in.
    """
    res = client.post(f"/login?email={unregistered_email}&password={password}")
    assert res.status_code == 404
    assert b'User not found, try again' in res.data


@pytest.mark.order(5)
def test_user_wrong_password(client):
    """Given the user credentials
    checking if the user could log in with the wrong password
    """
    res = client.post(f"/login?email={email}&password={wrong_password}")
    assert res.status_code == 401
    assert b"Password doesn't match, try again" in res.data


@pytest.mark.order(6)
def test_user_logout(client):
    """checking if the user could log out successfully"""
    res = client.post("/logout")
    assert res.status_code == 200
    assert b'User logged out Successfully' in res.data
