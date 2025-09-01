from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.routers import departments, hired_employees

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(departments.router,
                   prefix=settings.API_V1_STR,
                   tags=["departments"]
                   )

app.include_router(hired_employees.router,
                   prefix=settings.API_V1_STR,
                   tags=["hired_employees"])

@app.get("/")
def root():
    return {"message": "Globant Proposal for coding challenge"}
