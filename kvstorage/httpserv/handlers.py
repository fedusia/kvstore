from typing import Union
from pydantic import BaseModel, Field, StrictStr
from fastapi.requests import Request
from fastapi.responses import Response
from pydantic.error_wrappers import ValidationError
import json


class JSONRPCRequest(BaseModel):
    """
    Validating Data model for jsonrpc 2.0
    """

    jsonrpc: StrictStr = Field("2.0", const=True, example="2.0")
    id: Union[StrictStr, int] = Field(None, example=0)
    method: StrictStr
    params: dict


async def jsonrpc_dispatcher(request: Request, call_next):
    body = await request.body()
    try:
        JSONRPCRequest.validate(json.loads(body))
    except ValidationError as e:
        response = Response()
        response.body = bytes(e.json(), "UTF-8")
        response.headers["Content-type"] = "application/json"
        return response
    response = await call_next(request)
    return response


def hello_world():
    return "Hello world"


def getter(storage):
    def wrapped_getter(key):
        body = storage.get(key)
        return body

    return wrapped_getter


def setter(storage):
    def wrapped_setter(key, value):
        body = storage.set(key, value)
        return body

    return wrapped_setter
