from operator import methodcaller
from flask_mysqldb import MySQL
import requests
import json
from app import app
from config import mysql
from flask import jsonify
from datetime import date
from flask import flash, request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


@app.route("/")
def hello_world():
    return "Welcome to Migospay"


def CreateDebitTransationDetails(date, email, narration, credit, debit):
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor = mysql.connection.cursor()
    query = "insert into transaction_details (date, email, narration, credit, debit) values (%s, %s, %s, %s, %s)"
    bindData = (date, email, narration, credit, debit)
    cursor.execute(query, bindData)
    mysql.connection.commit()
    cursor.close()


@app.route("/api/login", methods=["POST"])
def login_user():
    _json = request.json
    _email = _json["email"]
    _password = _json["password"]

    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor = mysql.connection.cursor()
    query = "select email, phone from accounts where email = %s and password = %s"
    bindData = (_email, _password)
    cursor.execute(query, bindData)
    acc = cursor.fetchone()
    if acc:
        access_token = create_access_token(identity=_email)
        success = access_token
    else:
        return jsonify({"message": "Invalid username and password"}), 401

    return jsonify({"token": success, "data": acc, "message": "ok"}), 200


@app.route("/api/user", methods=["POST"])
def create_user():
    _json = request.json
    _email = _json["email"]
    _phone = _json["phone"]
    _password = _json["password"]

    fullname = "NULL"
    custID = "123456"
    cursor = mysql.connection.cursor()
    cursor.execute("select * from accounts where email = %s", [_email])
    acc = cursor.fetchone()
    if acc:
        return jsonify({"message": "User exists, Please Login"})
    else:
        query = "insert into accounts (email,phone,fullname,password,custID) values (%s, %s,%s, %s,%s)"
        bindData = (_email, _phone, _password, fullname, custID)
        cursor.execute(query, bindData)
        mysql.connection.commit()
        cursor.close()
        output = {
            "email": _email,
            "phone": _phone,
            "fullname": fullname,
            "custID": custID,
            "message": "ok",
        }

    return jsonify({"result": output}), 200


@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    #   return jsonify(logged_in_as=current_user),200
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor = mysql.connection.cursor()
    cursor.execute("select * from accounts where email = %s", current_user)
    userRows = cursor.fetchone()
    response = jsonify({"data": userRows})
    response.status_code = 200
    return response


@app.route("/api/profile", methods=["PUT"])
@jwt_required()
def edit_profile():
    current_user = get_jwt_identity()
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor = mysql.connection.cursor()

    _json = request.json
    _fullname = _json["fullname"]
    _phone = _json["phone"]
    _email = current_user

    query = "update accounts set fullname =%s , phone =%s where email = %s"
    bindData = (_fullname, _phone, _email)
    cursor.execute(query, bindData)
    mysql.connection.commit()
    cursor.close()

    output = {
        "email": current_user,
        "phone": _phone,
        "fullname": _fullname,
        "message": "ok",
    }

    return jsonify({"result": output}), 200


@app.route("/api/add_beneficiary", methods=["POST"])
@jwt_required()
def add_beneficiary():
    current_user = get_jwt_identity()

    _json = request.json
    _account_name = _json["account_name"]
    _account_number = _json["account_number"]
    _currency = _json["currency"]
    _beneficiary_name = _json["beneficiary_name"]
    _destination_branch_code = _json["destination_branch_code"]

    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor = mysql.connection.cursor()
    query = "insert into acc_beneficiary(account_name,account_number,currency,beneficiary_name, destination_branch_code, user) values (%s,%s,%s,%s,%s,%s)"
    bindData = (
        _account_name,
        _account_number,
        _currency,
        _beneficiary_name,
        _destination_branch_code,
        current_user,
    )
    cursor.execute(query, bindData)
    mysql.connection.commit()
    cursor.close()
    output = {"message": "ok"}
    return jsonify({"result": output}), 200


@app.route("/api/view_beneficiary", methods=["GET"])
@jwt_required()
def view_beneficiary():
    current_user = get_jwt_identity()
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor = mysql.connection.cursor()
    cursor.execute("select * from acc_beneficiary where user = %s", current_user)
    userRows = cursor.fetchone()
    response = jsonify({"data": userRows})
    response.status_code = 200
    return response


@app.route("/api/edit_beneficiary", methods=["PUT"])
@jwt_required()
def edit_beneficiary():
    current_user = get_jwt_identity()

    _json = request.json
    _account_name = _json["account_name"]
    _account_number = _json["account_number"]
    _currency = _json["currency"]
    _beneficiary_name = _json["beneficiary_name"]
    _destination_branch_code = _json["destination_branch_code"]

    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor = mysql.connection.cursor()
    # query = 'insert into acc_beneficiary(account_name,account_number,currency,beneficiary_name, destination_branch_code, user) values (%s,%s,%s,%s,%s,%s)'
    query = "update acc_beneficiary set account_name =%s, account_number =%s, currency=%s, beneficiary_name=%s, destination_branch_code=%s where user =%s "
    bindData = (
        _account_name,
        _account_number,
        _currency,
        _beneficiary_name,
        _destination_branch_code,
        current_user,
    )
    cursor.execute(query, bindData)
    mysql.connection.commit()
    cursor.close()
    output = {"message": "beneficiary update successful!"}
    return jsonify({"result": output}), 200


@app.route("/api/create-virtual-account", methods=["POST"])
@jwt_required()
def create_virtual_account():
    current_user = get_jwt_identity()
    _json = request.json
    _account_name = _json["account_name"]
    _email = current_user
    _bvn = _json["bvn"]
    _tx_ref = "VAL12"
    _phonenumber = _json["phonenumber"]
    _firstname = _json["firstname"]
    _lastname = _json["lastname"]
    _narration = _json["narration"]

    url = "https://api.flutterwave.com/v3/virtual-account-numbers"

    data = {
        "account_name": _account_name,
        "email": _email,
        "bvn": _bvn,
        "phonenumber": _phonenumber,
        "firstname": _firstname,
        "lastname": _lastname,
        "narration": _narration,
    }
    res = requests.post(
        url,
        data=json.dumps(data),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer FLWSECK_TEST-72fe360edef17334f4817a17407011bb-X",
        },
    )

    return jsonify({"result": res.json()}), 200


@app.route("/api/create-local-transfer", methods=["POST"])
@jwt_required()
def create_local_transfer():
    current_user = get_jwt_identity()
    _json = request.json
    _account_bank = _json["account_bank"]
    _account_number = _json["account_number"]
    _amount = _json["amount"]
    _narration = _json["narration"]
    _currency = _json["currency"]
    _reference = _json["reference"]
    _debit_currency = _json["debit_currency"]

    url = "https://api.flutterwave.com/v3/transfers"
    data = {
        "account_bank": _account_bank,
        "account_number": _account_number,
        "amount": _amount,
        "narration": _narration,
        "currency": _currency,
        "reference": _reference,
        "debit currency": _debit_currency,
    }
    res = requests.post(
        url,
        data=json.dumps(data),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer FLWSECK_TEST-72fe360edef17334f4817a17407011bb-X",
        },
    )

    today = str(date.today())

    CreateDebitTransationDetails(today, current_user, _narration, " ", _amount)

    return jsonify({"result": res.json()}), 200


@app.route("/api/create-intl-transfer", methods=["POST"])
@jwt_required()
def create_intl_transfer():
    current_user = get_jwt_identity()
    _json = request.json
    _account_bank = _json["account_bank"]
    _account_number = _json["account_number"]
    _amount = _json["amount"]
    _narration = _json["narration"]
    _currency = _json["currency"]
    _destination_branch_code = _json["destination_branch_code"]
    _reference = _json["reference"]
    _debit_currency = _json["debit_currency"]
    _beneficiary_name = _json["beneficiary_name"]

    url = "https://api.flutterwave.com/v3/transfers"
    data = {
        "account_bank": _account_bank,
        "account_number": _account_number,
        "destination_branch_code": _destination_branch_code,
        "amount": _amount,
        "narration": _narration,
        "currency": _currency,
        "reference": _reference,
        "beneficiary_name": _beneficiary_name,
        "debit currency": _debit_currency,
    }
    res = requests.post(
        url,
        data=json.dumps(data),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer FLWSECK_TEST-72fe360edef17334f4817a17407011bb-X",
        },
    )

    today = str(date.today())
    CreateDebitTransationDetails(today, current_user, _narration, " ", _amount)

    return jsonify({"result": res.json()}), 200


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        "status": 404,
        "message": "Record not found: " + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
