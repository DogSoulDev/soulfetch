
# Domain: Models for SoulFetch


from pydantic import BaseModel

class Request(BaseModel):
    method: str
    url: str
    headers: dict
    body: str

class Environment(BaseModel):
    name: str
    variables: dict

class History(BaseModel):
    method: str
    url: str
    status: int
    response: str

class Collection(BaseModel):
    name: str
    requests: list
