import uvicorn
from fastapi_jsonrpc import API
from kvstorage.httpserv.handlers import api_v1


def create_app():
    api = API()
    # logger = config_logger()
    # config = set_config()
    api.bind_entrypoint(api_v1)
    return api


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # <- config
