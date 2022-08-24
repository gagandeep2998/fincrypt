from decryption import decrypt
import pytest


@pytest.mark.order(18)
def test_decrypt():
    """Given the encrypted card details with key and nonce
    checking if the decrypt function is decrypting details correctly
    """
    card_details = {
        "card_number": "12345678",
        "cvv": "578",
        "expiry_month": "07",
        "expiry_year": "2022"
    }
    encrypted_details = {'card_number': b'\x19I\xdc\xc1\xfd\xd9\xf1/',
                         'cvv': b'M!\x7f',
                         'expiry_month': b'\xd3F',
                         'expiry_year': b'\xd2\x983\xa5'}

    key_nonce = {"key": b'\xf8\x9e\x11UNr\xd0\xc1\xdbx?\xab\x80\x8eO=',
                 "nonce": b'\x97]\xe0\xd1|\xfaW\xa8\x14\xa36#=\xba\xba\xda'}

    decrypted_details = decrypt(key_nonce["key"],
                                key_nonce["nonce"],
                                card_number=encrypted_details["card_number"],
                                cvv=encrypted_details["cvv"],
                                expiry_month=encrypted_details["expiry_month"],
                                expiry_year=encrypted_details["expiry_year"]
                                )

    assert decrypted_details["card_number"] == card_details["card_number"]
    assert decrypted_details["cvv"] == card_details["cvv"]
    assert decrypted_details["expiry_month"] == card_details["expiry_month"]
    assert decrypted_details["expiry_year"] == card_details["expiry_year"]
