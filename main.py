from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fincrypt.db"

db = SQLAlchemy(app)


# Card details table
class Cards(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    card_number = db.Column(db.BigInteger, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    expiry_month = db.Column(db.Integer, nullable=False)
    expiry_year = db.Column(db.Integer, nullable=False)
    key = db.Column(db.LargeBinary, nullable=False)
    nonce = db.Column(db.LargeBinary, nullable=False)


db.create_all()


@app.route("/")
def home():
    return "<h1>Welcome to the fincrypt api</h1>"


@app.route("/encrypt")
def encrypt():
    email = request.args.get("email")
    card_number = request.args.get("card_number")
    cvv = request.args.get("cvv")
    expiry_month = request.args.get("expiry_month")
    expiry_year = request.args.get("expiry_year")
    card_data = {
        "card_number": card_number,
        "cvv": cvv,
        "expiry_month": expiry_month,
        "expiry_year": expiry_year
    }

    key = get_random_bytes(16)

    print(key)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    print(nonce)
    encrypted_card_data = {}

    for card_field, data in card_data.items():
        encrypted_card_data[card_field] = cipher.encrypt(bytes(data, "UTF-8"))

    print(encrypted_card_data)

    new_card = Cards(
        email=email,
        card_number=encrypted_card_data["card_number"],
        cvv=encrypted_card_data["cvv"],
        expiry_month=encrypted_card_data["expiry_month"],
        expiry_year=encrypted_card_data["expiry_year"],
        key=key,
        nonce=nonce
    )
    db.session.add(new_card)
    db.session.commit()

    # cipher_text, tag = cipher.encrypt_and_digest(bytes(data, 'UTF-8'))

    return jsonify(success=" Data encrypted successfully ")


@app.route("/decrypt")
def decrypt():
    email = request.args.get("email")
    card = Cards.query.filter_by(email=email).first()
    key = card.key
    nonce = card.nonce

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    card_details = {
        "id": card.id,
        "card_number": int(cipher.decrypt(card.card_number)),
        "cvv": int(cipher.decrypt(card.cvv)),
        "expiry_month": int(cipher.decrypt(card.expiry_month)),
        "expiry_year": int(cipher.decrypt(card.expiry_year)),
    }
    print(card_details)

    return jsonify(card_details=[
        card_details
    ])


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
