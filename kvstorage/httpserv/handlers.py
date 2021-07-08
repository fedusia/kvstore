from pydantic import BaseModel, Field, StrictStr
from typing import Optional, List, Dict, Any, Union


class JSONRpcRequestModel(BaseModel):
    """
    Validating Data model for jsonrpc 2.0 request
    """

    jsonrpc: StrictStr = Field("2.0", const=True, example="2.0")
    id: Union[StrictStr, int] = Field(None, example=0)
    method: StrictStr
    params: dict


class JSONRpcResponseModel(BaseModel):
    """
    Validating Data model for jsonrpc 2.0 response
    """

    jsonrpc: StrictStr = Field("2.0", const=True, example="2.0")
    id: Union[StrictStr, int] = Field(None, example=0)
    result: Union[dict, str, int]


class JSONRpcErrorModel(BaseModel):
    loc: List[str]
    msg: str
    type: str
    ctx: Optional[Dict[str, Any]]


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


def hello_world(body: JSONRpcRequestModel):
    req = body.dict()
    data = "Hello {}".format(req["params"]["name"])
    resp = JSONRpcResponseModel(result=data, id=req["id"])
    return resp


def getter(storage):
    def wrapped_getter(body: JSONRpcRequestModel):
        req = body.dict()
        params = req["params"]
        data = storage.get(params["key"])
        resp = JSONRpcResponseModel(result=data, id=req["id"])
        return resp

    return wrapped_getter


def setter(storage):
    def wrapped_setter(body: JSONRpcRequestModel):
        req = body.dict()
        params = req["params"]
        data = storage.set(params["key"], params["value"])
        resp = JSONRpcResponseModel(result=data, id=req["id"])
        return resp
    return wrapped_setter
