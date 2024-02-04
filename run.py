import uvicorn

from src.config import (
    APP_WORKER,
    APP_HOST,
    APP_PORT
)

if __name__ == "__main__":

    uvicorn.run("src.main:app", host=APP_HOST,
                port=APP_PORT, workers=APP_WORKER, reload=True)
