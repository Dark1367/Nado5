from pydantic import BaseModel
from typing import List

class GenerateRequest(BaseModel):
    values: List[int]
    add_header: bool

class AccountRequest(BaseModel):
    btn: str
    index: int

class GeneratePDFRequest(BaseModel):
    problems: List[str]

class TemplateCreate(BaseModel):
    title: str
    repr: str