from pydantic import BaseModel, Field, StrictStr
from typing import Optional, List, Dict, Any, Union
from fastapi import Request
import json


from kvstorage.core.logic import JustPrint, PrintLogic
# class JSONRpcRequestModel:
#     """
#     Validating Data model for jsonrpc 2.0 request
#     """
#
#     jsonrpc: StrictStr = Field("2.0", const=True, example="2.0")
#     id: Union[StrictStr, int] = Field(None, example=0)
#     method: StrictStr
#     params: dict
#
#
# class JSONRpcResponseModel(BaseModel):
#     """
#     Validating Data model for jsonrpc 2.0 response
#     """
#
#     jsonrpc: StrictStr = Field("2.0", const=True, example="2.0")
#     id: Union[StrictStr, int] = Field(None, example=0)
#     result: Union[dict, str, int]
#
#
# class JSONRpcErrorModel(BaseModel):
#     loc: List[str]
#     msg: str
#     type: str
#     ctx: Optional[Dict[str, Any]]


# async def jsonrpc_dispatcher(request: Request, call_next):
#     body = await request.body()
#     try:
#         JSONRpcRequestModel.validate(json.loads(body))
#     except ValidationError as e:
#         response = Response()
#         response.body = bytes(e.json(), "UTF-8")
#         response.headers["Content-type"] = "application/json"
#         return response
#     response = await call_next(request)
#     return response

# def handle():
#     body = …
#     params = deserialize(parse(body))
#     logic = Logic()
#     logic.validate(params)
#     result = logic.execute(params)
#     response = serialize(response)
#     return response

# def hello_world(body: JSONRpcRequestModel):
#     req = body.dict()
#     data = "Hello {}".format(req["params"]["name"])
#     resp = JSONRpcResponseModel(result=data, id=req["id"])
#     return resp


def parse_body(body):
    return json.loads(body)


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
        "error": {
            "code": -32600,
            "message": "Invalid Request",
            "data": error_data
        },
    }
    return json.dumps(jsonrpc)


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
            version=params["jsonrpc"],
            id=params["id"],
            error_data=error_message
        )

    # serialize response
    data = serialize_to_jsonrpc(
        version=params["jsonrpc"],
        result=say_hello(
            params["params"]["name"]
        ),
        id=params["id"]
    )
    response = json.dumps(data)
    return response


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
