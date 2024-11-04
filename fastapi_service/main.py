from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from prometheus_client import generate_latest, Counter

import os
from uuid import uuid4
from routers import items, users
from utils.logger_config import app_logger

app = FastAPI()

os.makedirs("app_logs", exist_ok=True)

request_counter = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["operation", "method", "status"],
)


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    log_id = str(uuid4())
    with app_logger.contextualize(log_id=log_id):
        app_logger.info(f"Request to access {request.method} {request.url.path}")
        try:
            response = await call_next(request)
            if response.status_code == 422:
                app_logger.error(
                    f"Unprocessable Entity: {request.method} {request.url.path}"
                )
                request_counter.labels(
                    operation=request.url.path, method=request.method, status="422"
                ).inc()
            else:
                app_logger.info(
                    f"Request to {request.method} {request.url.path} successful"
                )
                request_counter.labels(
                    operation=request.url.path,
                    method=request.method,
                    status=str(response.status_code),
                ).inc()
        except RequestValidationError as ex:
            app_logger.error(
                f"Validation error for request to {request.method} {request.url.path}: {ex}"
            )
            request_counter.labels(
                operation=request.url.path, method=request.method, status="422"
            ).inc()
            response = JSONResponse(
                content={"success": False, "detail": ex.errors()}, status_code=422
            )
        except Exception as ex:
            app_logger.error(
                f"Request to {request.method} {request.url.path} failed: {ex}"
            )
            request_counter.labels(
                operation=request.url.path, method=request.method, status="500"
            ).inc()
            response = JSONResponse(content={"success": False}, status_code=500)
        finally:
            return response


# Include routers
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    app_logger.info("Root endpoint accessed")
    return {"Hello": "World"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
