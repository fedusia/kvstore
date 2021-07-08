import uvicorn
from fastapi import FastAPI, APIRouter

from kvstorage.httpserv.handlers import JSONRPCHandler
from kvstorage.storage.db import InMemStorage
from kvstorage.core.logic import Storage


def create_app():
    # logger = config_logger()
    # config = set_config()

    storage = Storage(engine=InMemStorage())

    api = FastAPI()

    router = APIRouter()
    router.add_api_route(path="/", endpoint=JSONRPCHandler(storage).dispatch_request, methods=["POST"])

    api.include_router(router)
    return api


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # <- config
