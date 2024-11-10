from pydantic import BaseModel


class LoginSchema(BaseModel):
    login: str
    password: str


class OutletSchema(BaseModel):
    guid: str
    name: str
    price_type_guid: str


class SuccessLoginSchema(BaseModel):
    login: str
    outlets: list[OutletSchema]
