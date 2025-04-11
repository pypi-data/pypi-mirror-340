import logging
import os
import time
import sys

import uvicorn
from Secweb import SecWeb
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from __version__ import version
from doorbeen.api.docs.meta import DocsMeta
from doorbeen.api.routers import PUBLIC_ROUTES
from doorbeen.core.config.execution_env import ExecutionEnv
from fastapi.logger import logger as fastapi_logger

API_PREFIX = "/api"
AUTH_PREFIX = "/auth"
API_VERSION_PREFIX = "/v1"
API_URL_PREFIX = API_PREFIX + API_VERSION_PREFIX
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 9001
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).split(API_PREFIX)[0]
print(ROOT_DIR)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


class CORSMiddlewareCustom(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "https://doorbeen.dev, http://frontend:3000"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers[
            "Access-Control-Allow-Headers"] = "Access-Control-Allow-Headers, Content-Type, Authorization, Accept, Access-Control-Allow-Origin, Set-Cookie"
        return response


if ExecutionEnv.https_enabled():
    SSL_KEYFILE = os.getenv("LOCAL_SSL_KEY")
    SSL_CERTIFICATE = os.getenv("LOCAL_SSL_CERT")

ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")
print(f"ALLOWED_ORIGINS: {ORIGINS}")

app = FastAPI(title="Doorbeen API", version=version, description=DocsMeta.API_GLOBAL_DESCRIPTION,
              docs_url=None, redoc_url=None, openapi_url=API_URL_PREFIX + "/openapi.json",
              openapi_tags=DocsMeta.TAGS_META,
              contact={"name": "Telescope Support", "url": "https://jointelescope.com",
                       "email": "info@jointelescope.com"})
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncIterator[None]:
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
#     yield

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())


# app.add_middleware(CORSMiddlewareCustom)

# FastAPIInstrumentor.instrument_app(app)
if not ExecutionEnv.is_local():
    print("Applying gunicorn headers in an non local environment")
    SecWeb(app=app, Option={
                            'coep': 'credentialless',
                            'coop': 'same-origin',
                            'xss': '1; mode=block',
                            'hsts': {'max-age': 31536000, 'includeSubDomains': True, 'preload': True},
                            'csp': {
                                'script-src': ["'self'", "'unsafe-eval'", "'unsafe-inline'", "cdn.jsdelivr.net"],
                                'img-src': ["'self'", "data:", "fastapi.tiangolo.com", "*"],
                                'style-src': ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
                                'connect-src': ["'self'", "*"],
                                'font-src': ["'self'", "data:", "fonts.scalar.com"]
                            }
                           })
    gunicorn_logger = logging.getLogger("gunicorn")
    log_level = gunicorn_logger.level

    root_logger = logging.getLogger()
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    gunicorn_access_logger = logging.getLogger("gunicorn.access")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")

    # Use gunicorn error handlers for root and fastapi loggers
    root_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.handlers = gunicorn_error_logger.handlers
    
    # Use gunicorn access handlers for uvicorn access logger
    if gunicorn_access_logger.handlers:
        uvicorn_access_logger.handlers = gunicorn_access_logger.handlers
    else:
        # If no access handlers, create a stream handler to stdout
        access_handler = logging.StreamHandler(sys.stdout)
        access_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
        ))
        uvicorn_access_logger.handlers = [access_handler]

    # Pass on logging levels
    root_logger.setLevel(log_level)
    uvicorn_access_logger.setLevel(log_level)
    fastapi_logger.setLevel(log_level)
    
    # Ensure propagation is enabled
    uvicorn_access_logger.propagate = True



for route in PUBLIC_ROUTES:
    app.include_router(route["router"], prefix=API_URL_PREFIX)


@app.get('/', tags=["Health"])
def health():
    return {"status": "running"}


# @app.options("/{path:path}")
# async def options_handler():
#     return JSONResponse(content="OK", headers={
#         "Access-Control-Allow-Origin": "https://doorbeen.dev",
#         "Access-Control-Allow-Credentials": "true",
#         "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
#         "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Content-Type, Authorization, Accept,"
#                                         " Access-Control-Allow-Origin, Set-Cookie"
#     })


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["cache-control"] = "no-store"
    return response


# if ExecutionEnv.is_profiling_enabled():
#     @app.middleware("http")
#     async def add_sql_tap(request: Request, call_next):
#         profiler = sqltap.start()
#         response = await call_next(request)
#         statistics = profiler.collect()
#         sqltap.report(statistics, "qa/reports/result.html", report_format="html")
#         return response
#
#
#     app.add_middleware(
#         PyInstrumentProfilerMiddleware,
#         server_app=app,  # Required to output the profile on server shutdown
#         profiler_output_type="html",
#         is_print_each_request=False,  # Set to True to show request profile on
#                                       # stdout on each request
#         open_in_browser=True,  # Set to true to open your web-browser automatically
#                                # when the server shuts down
#         html_file_name="qa/reports/fastapi/profile.html"  # Filename for output
#     )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "HEAD", "OPTIONS", "DELETE"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', "Accept",
                   'Access-Control-Allow-Origin', "Set-Cookie"]
)

reload_dirs = [os.path.join(ROOT_DIR, "api"), os.path.join(ROOT_DIR, "core")]


def start_api_server():
    if ExecutionEnv.https_enabled():
        uvicorn.run("doorbeen.api.main:app", host=SERVER_HOST, port=SERVER_PORT, reload=True, reload_dirs=reload_dirs,
                    ssl_keyfile=SSL_KEYFILE, ssl_certfile=SSL_CERTIFICATE, server_header=False)
    else:
        uvicorn.run("doorbeen.api.main:app", host=SERVER_HOST, port=SERVER_PORT, reload=True, reload_dirs=reload_dirs,
                    server_header=False)


if __name__ == "__main__":
    start_api_server()
