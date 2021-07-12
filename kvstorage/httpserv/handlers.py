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
            query = json.loads(body)
        except json.JSONDecodeError:
            error_message = "Not a valid JSON document"
            return self.jsonrpc_error(error_message)

        # validate
        checked = self.validate_jsonrpc(query)
        # do stuff/logic
        if not checked:
            error_message = "Not a valid jsonrpc request"
            return self.jsonrpc_error(error_data=error_message, req_id=query["id"])

        elif query["method"] == "set":
            if not query["params"].get("key") or not query["params"].get("value"):
                error_message = (
                    "Should specify params:{'key': <key>, 'value': <value> }"
                )
                return self.jsonrpc_error(error_data=error_message, req_id=query["id"])
            result = await self.setter(query["params"]["key"], query["params"]["value"])

        elif query["method"] == "get":
            result = await self.getter(query["params"]["key"])
            if not result:
                error_message = "No such key {}".format(query["params"]["key"])
                self.jsonrpc_error(error_data=error_message, req_id=query["id"])
        else:
            result = "Method not implemented"
            self.jsonrpc_error(error_data=result, req_id=query["id"])

        # serialize and send response
        return self.jsonrpc_success(result, req_id=query["id"])

    async def getter(self, key):
        return self.storage.get(key)

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
