from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship


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
