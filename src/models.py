from pydantic import BaseModel
from typing import List

class GenerateRequest(BaseModel):
    values: List[int]
    add_header: bool

class AccountRequest(BaseModel):
    btn: str
    index: int