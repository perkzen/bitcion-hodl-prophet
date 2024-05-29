import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from .routers import predict_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)


def create_server_config():
    server_config = uvicorn.Config(
        app="src.api.main:app",
        host="127.0.0.1",  # docker needs to have 0.0.0.0
        port=8000,
        reload=True,
        access_log=True,
        # log_config= None
        workers=1
    )

    return server_config


def run_server() -> None:
    server_config = create_server_config()
    server = uvicorn.Server(server_config)
    server.run()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    run_server()
