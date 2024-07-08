from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from mangum import Mangum
from src.app.routers import infraction, officer, person, vehicle, auth

app = FastAPI(title="N5", version="1.0", root_path="/dev/")

app.include_router(person.router, prefix="/person", tags=["person"])
app.include_router(vehicle.router, prefix="/vehicle", tags=["vehicle"])
app.include_router(officer.router, prefix="/officer", tags=["officer"])
app.include_router(infraction.router, prefix="/infraction", tags=["infraction"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
def root():
    return {"message": "Bienvenido al backend"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Traffic Violations API",
        version="1.0.0",
        description="API for managing traffic violations",
        routes=app.routes,
        servers=[{"url": "/dev/"}],
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

handler = Mangum(app)
