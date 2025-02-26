from fastapi import FastAPI
import requests

app = FastAPI()

# IP, куда будем отправлять данные (локальный сервер)
TARGET_IP = "http://127.0.0.1:5001"

@app.post("/send/")
def send_data(data: dict):
    """Принимаем данные и отправляем их на другой сервер"""
    try:
        response = requests.post(f"{TARGET_IP}/receive/", json=data)
        return {"status": "sent", "response": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def home():
    return {"message": "Сервер работает! Отправь POST-запрос на /send/"}

