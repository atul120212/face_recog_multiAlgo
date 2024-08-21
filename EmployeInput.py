from pydantic import BaseModel


class Employee(BaseModel):
    base64File: str
    id: str
    base64FileExt: str

