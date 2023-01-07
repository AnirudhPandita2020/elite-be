from pydantic import BaseModel


class CertificateResponse(BaseModel):
    certificate_id: str
    certificate_link: str
    type: str

    class Config:
        orm_mode = True
