from pydantic import BaseModel


# Card Schemas


class CardBody(BaseModel):
    card_number: str
    cvv: str
    expiry_month: str
    expiry_year: str


class CardResponse(BaseModel):
    id: int
    card_number: str
    cvv: str
    expiry_month: str
    expiry_year: str


class CardQuery(BaseModel):
    card_id: int


# User Authentication Models


class UserRegistration(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

