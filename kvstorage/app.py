import os
import uvicorn
from fastapi import FastAPI, APIRouter

from kvstorage.httpserv.handlers import JSONRPCHandler
from kvstorage.storage.db import InMemStorage
from kvstorage.core.logic import Storage
from kvstorage.core.config import ConfigLoader, JSONParser, ConfigLoaderException


def create_app(conf):
    # logger = config_logger()

    storage = Storage(engine=InMemStorage())

    api = FastAPI()

    router = APIRouter()
    router.add_api_route(
        path="/", endpoint=JSONRPCHandler(storage).dispatch_request, methods=["POST"]
    )

    api.include_router(router)
    return api


try:
    config = ConfigLoader(parser=JSONParser("config.json")).load_config()
except ConfigLoaderException:
    os.exit(1)

app = create_app(config)

if __name__ == "__main__":
    uvicorn.run(app, host=config["listen"], port=config["port"])  # <- config
