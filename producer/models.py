from pydantic import BaseModel


class MobileEntity(BaseModel):
    entity_id: str
    type: str
    longitude: str
    latitude: str


class Location(BaseModel):
    entity_id: MobileEntity
    type: str
    longitude: str
    latitude: str
