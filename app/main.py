from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, teams, players, attendances

app = FastAPI(
    title = "Asistencia CVLR API",
    description = "API para la gestion de asistencia de equipos deportivos",
    version = "1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(auth.router, prefix = "/api")
app.include_router(teams.router, prefix = "/api")
app.include_router(players.router, prefix = "/api")
app.include_router(attendances.router, prefix = "/api")


@app.get("/", tags = ["Health"])
async def root():
    return {"message": "API funcionando"}