from fastapi import FastAPI

app = FastAPI()

@app.post("/receive/")
def receive_data(data: dict):
    """Принимаем данные и возвращаем их"""
    print(f"Получены данные: {data}")
    return {"status": "received", "data": data}

@app.get("/")
def home():
    return {"message": "Принимающий сервер работает!"}

