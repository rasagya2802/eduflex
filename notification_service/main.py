from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Notification Service Running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "db": "not_required"}
