import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.base import BaseHTTPMiddleware

from kvstorage.httpserv.handlers import hello_world, setter, getter, jsonrpc_dispatcher
from kvstorage.storage.db import InMemStorage
from kvstorage.core.logic import Storage


def create_app():
    # logger = config_logger()
    # config = set_config()

    storage = Storage(engine=InMemStorage())

    api = FastAPI()
    # api.middleware("http")
    # api.add_middleware(BaseHTTPMiddleware, dispatch=jsonrpc_dispatcher)

    router = APIRouter()
    router.add_api_route(path="/", endpoint=hello_world, methods=["POST"])
    router.add_api_route(path="/get", endpoint=getter(storage), methods=["POST"])
    router.add_api_route(path="/set", endpoint=setter(storage), methods=["POST"])

    api.include_router(router)
    return api


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # <- config
