from pydantic import BaseModel


class CreateTruckDto(BaseModel):
    site: str
    trailer_number: str
    chasis_number: str
    engine_number: str
    trailer_length: int
    suspension: str

