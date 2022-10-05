from pydantic import BaseModel


class MobileEntity(BaseModel):
    id: str
    type: str
    description: str


class Movement(BaseModel):
    entity: MobileEntity
    longitude: str
    latitude: str
