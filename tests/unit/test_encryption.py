import pytest

from encryption import encrypt

@pytest.mark.order(17)
def test_encrypt():
    """Given the card details to encrypt function
    checking if it is encrypting details correctly.
    """
    encrypted_details, key_nonce = encrypt(card_number="12345678",
                                           cvv="578",
                                           expiry_month="07",
                                           expiry_year="2022")

    assert encrypted_details["card_number"] != "12345678"
    assert encrypted_details["cvv"] != "578"
    assert encrypted_details["expiry_month"] != "07"
    assert encrypted_details["expiry_year"] != "2022"
