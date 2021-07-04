from fastapi import FastAPI

from kvstorage import InMemStorage

app = FastAPI()

storage = InMemStorage()


@app.get("/")
async def hello_world():
    return "<p>Hello world</p>"


@app.get("/get")
def get(key):
    body = storage.get(key)
    return body


@app.put("/set")
def add(key, value):
    body = storage.set(key, value)
    return body
