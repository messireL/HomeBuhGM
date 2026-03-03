from fastapi import FastAPI
import uvicorn

from app.api.endpoints import router
from app.database.session import engine, Base
# Импортируем domain напрямую, чтобы SQLAlchemy гарантированно зарегистрировала модели
from app.models import domain 

# Создание таблиц при старте приложения
# Примечание: В будущем для миграций лучше использовать Alembic
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
except Exception as e:
    print(f"Error creating database tables: {e}")

app = FastAPI(
    title="Home Accounting System",
    description="Веб-приложение для учета финансов с шифрованием RSA/SHA-256",
    version="0.9.3-alpha"
)

# Подключение API роутера
app.include_router(router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def health_check():
    """Проверка статуса системы."""
    return {
        "status": "online", 
        "version": "0.9.3-alpha",
        "encryption": "RSA-2048/SHA-256",
        "database": "connected"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)