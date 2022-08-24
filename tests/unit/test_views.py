from tests.unit.test_auth import email, password
import json
import pytest

card_number = "1234568"
cvv = "567"
expiry_month = "07"
expiry_year = "2022"

edited_card_details = {
    "card_number": "8888888",
    "cvv": "777",
    "expiry_month": "08",
    "expiry_year": "2022"

}


def login_user(client):
    login_res = client.post(f"/login?email={email}&password={password}")
    assert login_res.status_code == 200


def logout_user(client):
    logout_res = client.post("/logout")
    assert logout_res.status_code == 200


@pytest.mark.order(7)
def test_home(client):
    """Given the home path
    checks if it is functioning correctly
    """
    res = client.get("/")
    assert res.status_code == 200
    assert b'Welcome to the fincrypt api' in res.data


@pytest.mark.order(8)
def test_add_new_card(client):
    """Given the card details
    checking if authorized user could add new card correctly
    """
    login_user(client)
    res = client.post(f"/add-card?card_number={card_number}&cvv={cvv}"
                      f"&expiry_month={expiry_month}&expiry_year={expiry_year}")
    assert res.status_code == 201
    assert b' Data encrypted and saved successfully ' in res.data


@pytest.mark.order(9)
def test_unauthorized_add_new_card(client):
    """Given the card details
    checking if unauthorized user could add card or not
    """
    logout_user(client)
    res = client.post(f"/add-card?card_number={card_number}&cvv={cvv}"
                      f"&expiry_month={expiry_month}&expiry_year={expiry_year}",
                      follow_redirects=True)
    assert res.status_code == 404
    assert b'User not found, try again' in res.data


@pytest.mark.order(10)
def test_get_cards(client):
    """Getting all the cards
    checking if authorized user can get his all card details
    """
    login_user(client)
    res = client.get("/get-cards")
    assert res.status_code == 200


@pytest.mark.order(11)
def test_unauthorized_get_cards(client):
    """Getting all the cards
    checking if the unauthorized user can get any card details
    """
    logout_user(client)
    res = client.get("/get-cards", follow_redirects=True)
    assert res.status_code == 404
    assert b'User not found, try again' in res.data


@pytest.mark.order(12)
def test_authorized_card_edit(client):
    """Edit the card details
    checking if the authorized user could edit his card details
    """

    login_user(client)
    all_cards = client.get("/get-cards")
    card_data = json.loads(all_cards.data.decode('utf-8'))
    card_id = card_data["card_details"][0]["id"]
    if card_id:
        res = client.put(f"/edit-card-details/{card_id}?"
                         f"card_number={edited_card_details['card_number']}&"
                         f"cvv={edited_card_details['cvv']}&"
                         f"expiry_month={edited_card_details['expiry_month']}&"
                         f"expiry_year={edited_card_details['expiry_year']}")
        assert res.status_code == 201
        assert b'Card details updated successfully' in res.data


@pytest.mark.order(13)
def test_unauthorized_card_edit(client):
    """Edit the card details
    checking if the authorized user could edit his card.
    """
    logout_user(client)
    random_card_id = 1
    res = client.put(f"/edit-card-details/{random_card_id}?"
                     f"card_number={edited_card_details['card_number']}&"
                     f"cvv={edited_card_details['cvv']}&"
                     f"expiry_month={edited_card_details['expiry_month']}&"
                     f"expiry_year={edited_card_details['expiry_year']}",
                     follow_redirects=True)

    assert res.status_code == 404
    assert b'User not found, try again' in res.data


@pytest.mark.order(14)
def test_delete_card_not_exist(client):
    """Deleting card details
    checking if the non-existing card details delete responses correctly
    """
    login_user(client)
    random_card_id = 100000
    res = client.delete(f"/delete/{random_card_id}")
    assert res.status_code == 404
    assert b'Card not found, please try again' in res.data


@pytest.mark.order(15)
def test_unauthorized_delete_card(client):
    """Deleting card details
    checking if unauthorized user could delete any card details
    """
    logout_user(client)
    random_card_id = 1
    res = client.delete(f"/delete/{random_card_id}", follow_redirects=True)
    assert res.status_code == 404
    assert b'User not found, try again' in res.data


@pytest.mark.order(16)
def test_delete_card(client):
    """Deleting card details
    checking if authorized user could delete his card details
    """
    login_user(client)
    all_cards = client.get("/get-cards")
    card_data = json.loads(all_cards.data.decode('utf-8'))
    card_id = card_data["card_details"][0]["id"]
    if card_id:
        res = client.delete(f"/delete/{card_id}")
        assert res.status_code == 200
        assert b'Card Details deleted successfully' in res.data
