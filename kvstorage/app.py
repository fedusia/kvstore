import uvicorn
from fastapi import FastAPI, APIRouter

from kvstorage.storage import InMemStorage
from kvstorage.core import Storage
from kvstorage.httpserv.handlers import getter, setter, hello_world


def create_app():
    api = FastAPI()

    # logger = config_logger()
    # config = set_config()
    storage = Storage(engine=InMemStorage())
    router = APIRouter()
    router.add_api_route("/", endpoint=hello_world, methods=["GET"])
    router.add_api_route("/get", endpoint=getter(storage), methods=["GET"])
    router.add_api_route("/set", endpoint=setter(storage), methods=["POST"])
    api.include_router(router)
    return api


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # <- config
