import json
from uuid import uuid4
from fastapi import Request
from kvstorage.core.logic import Storage
from kvstorage.core.logging import RequestIDAdapter
from fastapi import Response
from typing import Dict

# default handler do:
# 1. get data from signate
# 1. parse it and deserealize
# 1. Validate data
# 1. do some logic
# 1. serialize  response
# 1. return response


class JSONRPCHandler:
    def __init__(self, engine: Storage, logger: RequestIDAdapter):
        self.storage = engine
        self.logger = logger

    async def dispatch_request(self, request: Request) -> Response:
        req_id = str(request.headers.get("x-request-id", uuid4()))
        self.logger.extra = {"x-request-id": req_id}
        # get data from body
        body = await request.body()
        self.logger.info("raw request_body: {}".format(body.decode("UTF-8")))
        # deserialize
        try:
            query = json.loads(body)
            self.logger.info("Request data deserialized: {}".format(query))
        except json.JSONDecodeError:
            error_message = "Not a valid JSON document"
            self.logger.info("Failed to deserialize body: {}".format(error_message))
            return self.jsonrpc_error(error_message)

        # validate
        checked = self.validate_jsonrpc(query)
        if not checked:
            error_message = "Not a valid jsonrpc request"
            self.logger.info("error_message")
            return self.jsonrpc_error(
                error_data=error_message, request_id=req_id, jsonrpc_id=query["id"]
            )

        self.logger.info("Request validated")

        # do stuff/logic
        self.logger.info("Starting application logic")
        if query["method"] == "set":
            if not query["params"].get("key") or not query["params"].get("value"):
                error_message = (
                    "Should specify params:{'key': <key>, 'value': <value> }"
                )
                self.logger.error("{}".format(error_message))
                return self.jsonrpc_error(
                    error_data=error_message, request_id=req_id, jsonrpc_id=query["id"]
                )
            result = await self.setter(query["params"]["key"], query["params"]["value"])
            self.logger.info("{}".format(result))

        elif query["method"] == "get":
            result = await self.getter(query["params"]["key"])
            self.logger.info("{}".format(result))
            if not result:
                error_message = "No such key {}".format(query["params"]["key"])
                self.jsonrpc_error(
                    error_data=error_message, request_id=req_id, jsonrpc_id=query["id"]
                )
        else:
            result = "Method not implemented"
            self.logger.error("{}".format(result))
            self.jsonrpc_error(
                error_data=result, request_id=req_id, jsonrpc_id=query["id"]
            )

        # serialize and send response
        self.logger.info("Serialize data and send response: {}".format(result))
        return self.jsonrpc_success(result, request_id=req_id, jsonrpc_id=query["id"])

    async def getter(self, key):
        return self.storage.get(key)

    async def setter(self, key, value):
        data = self.storage.set(key, value)
        return data

    @staticmethod
    def jsonrpc_error(error_data, request_id, jsonrpc_id=None) -> Response:
        jsonrpc = {
            "jsonrpc": "2.0",
            "error": {"code": -32600, "message": "Invalid Request", "data": error_data},
        }
        if jsonrpc_id:
            jsonrpc["id"] = jsonrpc_id
        response = Response()
        response.headers["X-Request-Id"] = request_id
        response.headers["Content-type"] = "application/json"

        body = json.dumps(jsonrpc)
        response.body = body.encode("UTF-8")

        return response

    @staticmethod
    def validate_jsonrpc(data: Dict) -> bool:
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
    def jsonrpc_success(result, request_id, jsonrpc_id=None) -> Response:
        data = {"jsonrpc": "2.0", "result": result}
        if not jsonrpc_id:
            return
        data["id"] = jsonrpc_id
        response = Response()
        response.headers["X-Request-Id"] = request_id
        response.headers["Content-type"] = "application/json"

        body = json.dumps(data)
        response.body = body.encode("UTF-8")
        return response
