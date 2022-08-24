from Crypto.Cipher import AES


def decrypt(key, nonce, **kwargs):
    # print(key, nonce)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = {}
    for details, value in kwargs.items():
        # print(details, value)
        decrypted_data[details] = str(cipher.decrypt(value).decode("UTF-8"))
    return decrypted_data
