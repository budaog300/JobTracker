from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as router_auth
from src.modules.vacancies.router import router as router_vacancies
from src.modules.companies.router import router as router_companies


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", summary="Проверка сервера")
async def health():
    return {"message": "ok"}


app.include_router(router_auth)
app.include_router(router_vacancies)
app.include_router(router_companies)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
