from pydantic import BaseModel


class RecorgoniseObject(BaseModel):    
    Empid: str
    confidence:str