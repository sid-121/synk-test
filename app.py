# for logging
import logging
import os

import bugsnag
from bugsnag.asgi import BugsnagMiddleware
from logutils.config import setup_loghandlers
from middleware.lifespan import LifeSpanMiddleware
from middleware.liveness import LivenessMiddleware
from middleware.logger import LoggingMiddleware
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from .config import BUGSNAG_API_KEY, DEBUG, RELEASE_STAGE
from .urls import url_patterns

setup_loghandlers(app_name=".".join(__name__.split(".")[:-1]))
logger = logging.getLogger(__name__)

bugsnag.configure(
    api_key=BUGSNAG_API_KEY, project_root=os.getcwd(), release_stage=RELEASE_STAGE
)


routes = [
    Mount(
        "/static",
        app=StaticFiles(directory="cms_app/platform/app_bundle"),
        name="static",
    )
]

app = Starlette(routes=routes, debug=DEBUG, lifespan=LifeSpanMiddleware)

app.add_middleware(LivenessMiddleware)
app.add_middleware(BugsnagMiddleware)
app.add_middleware(LoggingMiddleware)


for url in url_patterns:
    app.add_route(url[0], url[1])


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Exception Handler for 404 Page not Found
    :param request:
    :param exc:
    :return: Json Response
    """
    return JSONResponse(
        {"status": "error", "message": "Page not found"}, status_code=exc.status_code
    )


@app.exception_handler(405)
async def method_not_allowed(request, exc):
    """
    Exception Handler for 405 MEthod Not Allowed
    :param request:
    :param exc:
    :return: Json Response
    """
    return JSONResponse(
        {"status": "error", "message": "Method Not Allowed"}, status_code=405
    )


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Exception Handler for 500 Internal Server Error
    :param request:
    :param exc:
    :return: Json Response
    """
    return JSONResponse(
        {"status": "error", "message": "Server error. Please contact storelocal"},
        status_code=500,
    )
