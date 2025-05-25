from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def configure_app(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Podés ajustar esto
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
