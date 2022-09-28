from pydantic import BaseModel


class Location(BaseModel):
    entity_id: str
    type: str
    longitude: str
    latitude: str
