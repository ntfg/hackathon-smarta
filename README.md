Для запуска нужно создать в директории с проектом файл .env с содержанием
```
ALLOWED_USER = <значение>
JWT_KEY = <значение>
API_ID = <значение>
API_HASH = <значение>
BOT_TOKEN = <значение>
SERVER_IP = <значение>
SERVER_PORT = <значение>
```

Прописать команды
```
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
python3 app.py
```
