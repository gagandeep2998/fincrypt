from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from .models import Cards
from . import db
from decryption import decrypt
from encryption import encrypt
from flask_pydantic import validate
from .schemas import CardBody, CardResponse, CardQuery


views = Blueprint("views", __name__)


@views.route("/")
def home():
    return jsonify(Welcome="Welcome to the fincrypt api")


@views.route("/cards", methods=["POST"])
@login_required
@validate()
def add_new_card(body: CardBody):
    card_number = body.card_number
    cvv = body.cvv
    expiry_month = body.expiry_month
    expiry_year = body.expiry_year

    encrypted_card_details, key_and_nonce = encrypt(card_number=card_number,
                                                    cvv=cvv,
                                                    expiry_month=expiry_month,
                                                    expiry_year=expiry_year,
                                                    )

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

    return jsonify(success=" Data encrypted and saved successfully "), 201


@views.route("/cards")
@login_required
@validate(response_many=True)
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
        all_cards.append(card_details)

    return [CardResponse(id=card['id'],
                         card_number=card['card_number'],
                         cvv=card['cvv'],
                         expiry_month=card['expiry_month'],
                         expiry_year=card['expiry_year']) for card in all_cards]


@views.route("/cards", methods=["DELETE"])
@login_required
@validate()
def delete_card(query: CardQuery):
    current_user_id = current_user.get_id()
    all_cards = db.session.query(Cards).filter_by(user_id=current_user_id).all()
    card_to_delete = None
    for card in all_cards:
        if card.id == query.card_id:
            card_to_delete = card

    if not card_to_delete:
        return jsonify(Error="Card not found, please try again"), 404

    db.session.delete(card_to_delete)
    db.session.commit()
    return jsonify(success="Card Details deleted successfully"), 200


@views.route("/cards", methods=["PUT"])
@login_required
@validate()
def edit_card(query: CardQuery, body: CardBody):
    current_user_id = current_user.get_id()
    all_cards = db.session.query(Cards).filter_by(user_id=current_user_id).all()
    card_to_update = None
    for card in all_cards:
        if card.id == query.card_id:
            card_to_update = card

    if not card_to_update:
        return jsonify(Error="Card not found, please try again"), 404

    card_number = body.card_number
    cvv = body.cvv
    expiry_month = body.expiry_month
    expiry_year = body.expiry_year

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
