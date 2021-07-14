import sys
import os
import logging
import uvicorn
from fastapi import FastAPI, APIRouter


from kvstorage.httpserv.handlers import JSONRPCHandler
from kvstorage.storage.db import InMemStorage
from kvstorage.core.logic import Storage
from kvstorage.core.config import ConfigLoader, JSONParser, ConfigLoaderException
from kvstorage.core.logging import create_logger


def create_app():
    # # Logger initialization
    logger = create_logger()

    # FastApi and config initialization
    api = FastAPI()
    try:
        conf_path = os.getenv("APP_CONF_PATH", default="config.json")
        api.conf = ConfigLoader(parser=JSONParser(conf_path)).load_config()
    except ConfigLoaderException:
        raise
        sys.exit(1)

    storage = Storage(engine=InMemStorage())

    router = APIRouter()
    router.add_api_route(
        path="/",
        endpoint=JSONRPCHandler(storage, logger).dispatch_request,
        methods=["POST"],
    )

    api.include_router(router)
    return api


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host=app.conf["listen"], port=app.conf["port"])  # <- config
