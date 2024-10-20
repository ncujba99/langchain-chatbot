from fastapi import FastAPI
import uvicorn
from api.chat.endpoints import router as chat_router

app = FastAPI()
app.include_router(chat_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
