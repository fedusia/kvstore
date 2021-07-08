from fastapi import Request
import json

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


def say_hello(name):
    return "Hello, {}".format(name)


def serialize_to_jsonrpc(version, result, id):
    jsonrpc = {
        "jsonrpc": version,
        "id": id,
        "result": result,
    }
    return jsonrpc


def jsonrpc_error(version, id, error_data):
    jsonrpc = {
        "jsonrpc": version,
        "id": id,
        "error": {"code": -32600, "message": "Invalid Request", "data": error_data},
    }
    return json.dumps(jsonrpc)


def jsonrpc_success(params):
    data = serialize_to_jsonrpc(
        version=params["jsonrpc"],
        result=say_hello(params["params"]["name"]),
        id=params["id"],
    )
    response = json.dumps(data)
    return response


async def hello_world(request: Request):
    # get body
    body = await request.body()
    # deserialize
    params = json.loads(body)
    # validate
    checked = validate_jsonrpc(params)
    # do stuff/logic
    if not checked:
        error_message = "Not a valid jsonrpc request"
        return jsonrpc_error(
            version=params["jsonrpc"], id=params["id"], error_data=error_message
        )
    # serialize and send response
    return jsonrpc_success(params)


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
