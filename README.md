# Fincrypt
An API that will encrypt and store debit card details with the help of AES Encryption Algorithm

## Introduction
Fincrypt is an API which will store your debit card details safely in an Encrypted format. When we talk about the financial details these are sensitive details and need to be saved safely when we encrypt details and save then the authorized user can see the card details. Nowadays, a lot of data breaches are happening and this API can act as a safe wallet to save your card details.

## Requirements 
You can see the requirements.txt to see the requirements.
You can also install the requirements with `pip`

```pip install requirements.txt ```
## How to use 
First you need to register with name, email id and password to start using this API


### Registration
User registration Endpoint 
```http
POST /register?name=demo&email=demo@email.com&password=12345678
```
| Parameter  | Type | Description                |
|:-----------| :--- |:---------------------------|
| `name`     | `String`| **Required** Your Name     |
| `email`    | `String`| **Required** Your Email    |
| `password` | `String`| **Required** Your Password |

### User Login
After registration, you need to log in with email and password

User login Endpoint
```http
POST /login?email=demo@email.com&password=12345678
```
| Parameter  | Type | Description                |
|:-----------| :--- |:---------------------------|
| `email`    | `String`| **Required** Your Email    |
| `password` | `String`| **Required** Your Password |

### Add Card Details
After login successfully, Now you can add your Debit Card Details

Add New Card Endpoint
```http
POST /add-card?card_number=12345678&cvv=567&expiry_month=07&expiry_year=2024
```
| Parameter      | Type     | Description                               |
|:---------------|:---------|:------------------------------------------|
| `card_number`  | `String` | **Required** Your Debit Card Number       |
| `cvv`          | `String` | **Required** Your Debit Card cvv          |
| `expiry_month` | `String` | **Required** Your Debit Card Expiry Month |
| `expiry_year`  | `String` | **Required** Your Debit Card Expiry Year  |

### Get All Card Details

You can see all the cards you have added

Get All Card Endpoint
```http
GET /get-cards
```

**Note**
Log in is required to get all the cards

### Edit Any Card Details
```http
PUT /edit-card-details/{YOUR CARD ID IN INTEGER}?card_number=12345558&cvv=577&expiry_month=09&expiry_year=2025
```
**Note**
Log in is required to edit card details

Example: http://127.0.0.1/edit-card-details/1?card_number=12345558&cvv=577&expiry_month=09&expiry_year=2025

| Parameter      | Type     | Description                               |
|:---------------|:---------|:------------------------------------------|
| `card_number`  | `String` | **Required** Your Debit Card Number       |
| `cvv`          | `String` | **Required** Your Debit Card cvv          |
| `expiry_month` | `String` | **Required** Your Debit Card Expiry Month |
| `expiry_year`  | `String` | **Required** Your Debit Card Expiry Year  |


### Delete Your Card Details

Delete your Card Details 

Delete Card Details Endpoint
```http
DELETE /delete/{YOUR CARD ID IN INTEGER}
```
**Note**
Log in is required to delete card details

Example: http://127.0.0.1/delete/1

### Log Out User
You can also log out

Log out user Endpoint
```http
POST /logout
```






