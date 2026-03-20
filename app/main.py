import uvicorn
from fastapi import FastAPI
from api.routes import router as shortener_router


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

# Routes connect
app.include_router(shortener_router)

async def run():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
        #reload=True
    )

if __name__ == "__main__":
    run()