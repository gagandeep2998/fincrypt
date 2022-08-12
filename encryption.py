from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt(**kwargs):
    key = get_random_bytes(16)
    print(key)

    cipher = AES.new(key, AES.MODE_EAX)

    nonce = cipher.nonce
    print(nonce)
    encrypted_details = {}
    key_and_nonce = {
        "key": key,
        "nonce": nonce
    }
    for key, detail in kwargs.items():
        # print(key, detail)
        encrypted_details[key] = cipher.encrypt(bytes(detail, 'UTF-8'))

    return encrypted_details, key_and_nonce
