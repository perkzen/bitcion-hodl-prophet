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


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


app.include_router(predict_router)


def run_server() -> None:
    uvicorn.run(app="src.api.main:app", host="0.0.0.0", port=8000, reload=True, access_log=True)


if __name__ == "__main__":
    run_server()
