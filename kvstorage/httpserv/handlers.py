from fastapi import Request
import json
from json import JSONDecodeError

# default handler do:
# 1. get data from signate
# 1. parse it and deserealize
# 1. Validate data
# 1. do some logic
# 1. serialize  response
# 1. return response


def validate_jsonrpc(data: dict):
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


async def say_hello(name):
    return "Hello, {}".format(name)


def jsonrpc_error(error_data, req_id=None):
    jsonrpc = {
        "jsonrpc": "2.0",
        "error": {"code": -32600, "message": "Invalid Request", "data": error_data},
    }
    if req_id:
        jsonrpc["id"] = req_id
    response = json.dumps(jsonrpc)
    return response


def jsonrpc_success(result, req_id=None):
    data = {"jsonrpc": "2.0", "result": result}
    if not req_id:
        return
    data["id"] = req_id
    response = json.dumps(data)
    return response


async def hello_world(request: Request):
    # get body
    body = await request.body()

    # deserialize
    try:
        params = json.loads(body)
    except JSONDecodeError:
        error_message = "Not a valid JSON document"
        return jsonrpc_error(error_message)

    # validate
    checked = validate_jsonrpc(params)
    # do stuff/logic
    if not checked:
        error_message = "Not a valid jsonrpc request"
        return jsonrpc_error(error_data=error_message, reqid=params["id"])

    result = await say_hello(params["params"]["name"])
    # serialize and send response
    return jsonrpc_success(result, req_id=params["id"])


# def getter(storage):
#     def wrapped_getter(body: JSONRpcRequestModel):
#         req = body.dict()
#         params = req["params"]
#         data = storage.get(params["key"])
#         resp = JSONRpcResponseModel(result=data, id=req["id"])
#         return resp
#
#     return wrapped_getter
#
#
# def setter(storage):
#     def wrapped_setter(body: JSONRpcRequestModel):
#         req = body.dict()
#         params = req["params"]
#         data = storage.set(params["key"], params["value"])
#         resp = JSONRpcResponseModel(result=data, id=req["id"])
#         return resp
#
#     return wrapped_setter
