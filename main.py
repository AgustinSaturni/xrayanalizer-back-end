from fastapi import FastAPI
from core.config import configure_app
from api.endpoints import projects, reports, images  # ✅ importamos el nuevo router

app = FastAPI()

# Configurar CORS, middlewares, etc.
configure_app(app)

# Incluir los routers
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(images.router, prefix="/images", tags=["Images"])  # ✅ nuevo router
