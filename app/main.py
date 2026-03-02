from fastapi import FastAPI
from app.api.endpoints import router
from app.database.session import engine, Base
from app.models import domain  # Импорт для регистрации моделей в Base

# Автоматическое создание таблиц при старте (для Alpha-версии)
# В продакшене рекомендуется использовать Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Home Accounting",
    description="Веб-приложение Домашняя бухгалтерия с шифрованием RSA/SHA",
    version="0.4.0-alpha"
)

# Подключение маршрутов API
app.include_router(router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """Приветственное сообщение и проверка работоспособности."""
    return {
        "status": "online",
        "message": "Система Домашней Бухгалтерии готова к работе",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)