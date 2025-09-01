from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.routers import departments, hired_employees, jobs
from app.core.logging_config import logger

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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        logger.info(f"{request.method} {request.url} -> {response.status_code}\n{response}")
        return response
    except Exception as e:
        logger.error(f"Error en {request.method} {request.url}: {e}")
        raise e

app.include_router(departments.router,
                   prefix=settings.API_V1_STR,
                   tags=["departments"]
                   )

app.include_router(hired_employees.router,
                   prefix=settings.API_V1_STR,
                   tags=["hired_employees"])

app.include_router(jobs.router,
                   prefix=settings.API_V1_STR,
                   tags=["jobs"])

@app.get("/")
def root():
    return {"message": "Globant Proposal for coding challenge"}
