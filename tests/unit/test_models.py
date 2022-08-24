from fincrypt.models import User, Cards
import pytest
from tests.conftest import cleaning_test_db


@pytest.mark.order(19)
def test_user_model(client):
    """Given a User model
    when new User is created
    then check all the fields are defined correctly
    """
    new_user = User(name="Demo",
                    email="demo@email.com",
                    password="12345678")
    assert new_user.name == "Demo"
    assert new_user.email == "demo@email.com"
    assert new_user.password == "12345678"


@pytest.mark.order(20)
def test_cards_model(client):
    """Given a Cards model
    when a new card is created
    then check all the fields are defined correctly
    """
    new_card = Cards(
        card_number="12345678",
        cvv="578",
        expiry_month="07",
        expiry_year="2022"
    )
    assert new_card.card_number == "12345678"
    assert new_card.cvv == "578"
    assert new_card.expiry_month == "07"
    assert new_card.expiry_year == "2022"
    cleaning_test_db()
