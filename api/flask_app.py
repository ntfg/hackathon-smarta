from flask import Flask, request, jsonify
import datetime
from data import Database
import jwt 
import os

app = Flask(__name__)

db = Database()

@app.route("/get")
def get():
    # Если появится ошибка, значит токен зашифрован другим ключом, или у него истек срок действия, или его вообще нет в заголовке
    try:
        token = request.headers.get("Authorization").split()[1]
        jwt.decode(token, os.getenv("JWT_KEY"), algorithms="HS256")
    except:
        return "Недействительный токен"
   

    date = request.args.get("date", type=str)

    if date:
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            print(date)
            return jsonify(db.get_by_date(date))
        except:
            return "Невверный формат поля дата.\nОжидается ГГГГ-ММ-ДД"
        
    
    return jsonify(db.get_any())

