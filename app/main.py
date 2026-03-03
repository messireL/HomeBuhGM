from fastapi import FastAPI
from app.api.endpoints import router
from app.database.session import engine, Base
# Важно импортировать все модели для их создания в БД
from app.models import domain 

# Автоматическое создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Home Accounting System",
    description="Система учета финансов с RSA-шифрованием данных",
    version="0.9.2-alpha"
)

# Подключение маршрутов
app.include_router(router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def health_check():
    """Проверка доступности сервиса."""
    return {
        "status": "active", 
        "version": "0.9.2-alpha",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)