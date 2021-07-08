from fastapi import Request
import json
from kvstorage.core.logic import Storage

# default handler do:
# 1. get data from signate
# 1. parse it and deserealize
# 1. Validate data
# 1. do some logic
# 1. serialize  response
# 1. return response


async def say_hello(name):
    return "Hello, {}".format(name)


class JSONRPCHandler:
    def __init__(self, engine: Storage):
        self.storage = engine

    async def dispatch_request(self, request: Request):
        # get data from body
        body = await request.body()

        # deserialize
        try:
            params = json.loads(body)
        except json.JSONDecodeError:
            error_message = "Not a valid JSON document"
            return self.jsonrpc_error(error_message)

        # validate
        checked = self.validate_jsonrpc(params)
        # do stuff/logic
        if not checked:
            error_message = "Not a valid jsonrpc request"
            return self.jsonrpc_error(error_data=error_message, req_id=params["id"])

        if params["method"] == "say_hello":
            result = await self.say_hello(params["params"]["name"])

        elif params["method"] == "set":
            result = await self.setter(
                params["params"]["key"], params["params"]["value"]
            )

        elif params["method"] == "get":
            result = await self.getter(params["params"]["key"])
        else:
            result = "Method not implemented"
            self.jsonrpc_error(error_data=result, req_id=params["id"])

        # serialize and send response
        return self.jsonrpc_success(result, req_id=params["id"])

    async def getter(self, key):
        value = self.storage.get(key)
        if value:
            return value
        return None

    async def setter(self, key, value):
        data = self.storage.set(key, value)
        return data

    @staticmethod
    async def say_hello(name):
        return "Hello, {}".format(name)

    @staticmethod
    def jsonrpc_error(error_data, req_id=None):
        jsonrpc = {
            "jsonrpc": "2.0",
            "error": {"code": -32600, "message": "Invalid Request", "data": error_data},
        }
        if req_id:
            jsonrpc["id"] = req_id
        response = json.dumps(jsonrpc)
        return response

    @staticmethod
    def validate_jsonrpc(data):
        try:
            if not data["jsonrpc"] == "2.0":
                return False
            elif not data["method"]:
                return False
            elif not data["id"]:
                return False
            elif not data["params"] and not isinstance(data["params"], dict):
                return False
        except KeyError:
            return False
        return True

    @staticmethod
    def jsonrpc_success(result, req_id=None):
        data = {"jsonrpc": "2.0", "result": result}
        if not req_id:
            return
        data["id"] = req_id
        response = json.dumps(data)
        return response
