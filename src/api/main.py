import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.model.helpers.mlflow import download_model_registry
from .routers import predict_router, price_router, audit_log_router, metrics_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.put("/update-model-registry")
def update_model_registry() -> dict[str, str]:
    return download_model_registry()


app.include_router(predict_router)
app.include_router(price_router)
app.include_router(audit_log_router)
app.include_router(metrics_router)


def run_server() -> None:
    uvicorn.run(app="src.api.main:app", host="127.0.0.1", port=8000, reload=True, access_log=True)


if __name__ == "__main__":
    run_server()
