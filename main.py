from flask import Flask, request, jsonify
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from encryption import encrypt
from decryption import decrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fincrypt.db"

app.config["SECRET_KEY"] = "This is some secret data"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Card details table
class Cards(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="cards")
    card_number = db.Column(db.BigInteger, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    expiry_month = db.Column(db.Integer, nullable=False)
    expiry_year = db.Column(db.Integer, nullable=False)
    key = db.Column(db.LargeBinary, nullable=False)
    nonce = db.Column(db.LargeBinary, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    cards = relationship("Cards", back_populates="user")


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/register", methods=["POST", "GET"])
def register():
    name = request.args.get("name")
    email = request.args.get("email")
    password = request.args.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(
            Error="You are already registered with this email, login instead"
        ), 409

    hash_and_salt_password = generate_password_hash(
        password,
        method="pbkdf2:sha256",
        salt_length=8,
    )

    new_user = User(
        email=email,
        password=hash_and_salt_password,
        name=name
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(success="User registered successfully"), 200


@app.route("/login", methods=["POST", "GET"])
def login():
    email = request.args.get("email")
    password = request.args.get("password")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(
            Error="User not found, try again"
        ), 404

    hash_password = user.password
    if check_password_hash(hash_password, password):
        login_user(user)
        return jsonify(Success="User loggedIn Successfully"), 200
    else:
        return jsonify(Error="Password doesn't match, try again"), 403


@app.route("/logout")
def logout():
    logout_user()
    return jsonify(Success="User logged out Successfully")


@app.route("/")
def home():
    return "<h1>Welcome to the fincrypt api</h1>"


@app.route("/add-card", methods=["GET", "POST"])
@login_required
def add_new_card():
    card_number = request.args.get("card_number")
    cvv = request.args.get("cvv")
    expiry_month = request.args.get("expiry_month")
    expiry_year = request.args.get("expiry_year")

    encrypted_card_details, key_and_nonce = encrypt(card_number=card_number,
                                                    cvv=cvv,
                                                    expiry_month=expiry_month,
                                                    expiry_year=expiry_year,
                                                    )

    print(encrypted_card_details)

    new_card = Cards(
        card_number=encrypted_card_details["card_number"],
        cvv=encrypted_card_details["cvv"],
        expiry_month=encrypted_card_details["expiry_month"],
        expiry_year=encrypted_card_details["expiry_year"],
        key=key_and_nonce["key"],
        nonce=key_and_nonce["nonce"],
        user=current_user,
    )
    db.session.add(new_card)
    db.session.commit()

    return jsonify(success=" Data encrypted and saved successfully ")


@app.route("/get-cards")
@login_required
def get_cards():
    current_user_id = current_user.get_id()
    cards = db.session.query(Cards).filter_by(user_id=current_user_id).all()
    all_cards = []
    for card in cards:
        key = card.key
        nonce = card.nonce

        decrypted_data = decrypt(key,
                                 nonce,
                                 card_number=card.card_number,
                                 cvv=card.cvv,
                                 expiry_month=card.expiry_month,
                                 expiry_year=card.expiry_year)
        card_details = {
            "id": card.id,
            "card_number": int(decrypted_data["card_number"]),
            "cvv": int(decrypted_data["cvv"]),
            "expiry_month": int(decrypted_data["expiry_month"]),
            "expiry_year": int(decrypted_data["expiry_year"]),
        }
        print(card_details)
        all_cards.append(card_details)

    return jsonify(card_details=all_cards)


@app.route("/delete/<int:card_id>", methods=["GET", "DELETE"])
@login_required
def delete_card(card_id):
    current_user_id = current_user.get_id()
    all_cards = db.session.query(Cards).filter_by(user_id=current_user_id).all()
    card_to_delete = None
    for card in all_cards:
        if card.id == card_id:
            card_to_delete = card

    if not card_to_delete:
        return jsonify(Error="Card not found, please try again"), 404

    db.session.delete(card_to_delete)
    db.session.commit()
    return jsonify(success="Card Details deleted successfully"), 200


@app.route("/edit-card-details/<int:card_id>")
@login_required
def edit_card(card_id):
    current_user_id = current_user.get_id()
    all_cards = db.session.query(Cards).filter_by(user_id=current_user_id).all()
    card_to_update = None
    for card in all_cards:
        if card.id == card_id:
            card_to_update = card

    if not card_to_update:
        return jsonify(Error="Card not found, please try again"), 404

    card_number = request.args.get("card_number")
    cvv = request.args.get("cvv")
    expiry_month = request.args.get("expiry_month")
    expiry_year = request.args.get("expiry_year")

    encrypted_details, key_and_nonce = encrypt(
        card_number=card_number,
        cvv=cvv,
        expiry_month=expiry_month,
        expiry_year=expiry_year,
    )
    card_to_update.card_number = encrypted_details["card_number"]
    card_to_update.cvv = encrypted_details["cvv"]
    card_to_update.expiry_month = encrypted_details["expiry_month"]
    card_to_update.expiry_year = encrypted_details["expiry_year"]
    card_to_update.key = key_and_nonce["key"]
    card_to_update.nonce = key_and_nonce["nonce"]

    db.session.commit()

    return jsonify(Success="Card details updated successfully"), 201


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
