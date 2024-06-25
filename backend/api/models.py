from typing import List, Optional
from pydantic import BaseModel, Field

class IdolInput(BaseModel):
    stage_name: str
    real_name: str
    group: str

class GroupIdolInput(BaseModel):
    stage_name: str
    real_name: str

class GroupInput(BaseModel):
    name: str
    company: str
    idols: Optional[List[GroupIdolInput]]

class IdolUpdate(BaseModel):
    id: int
    stage_name: Optional[str]
    real_name: Optional[str]
    group: Optional[str]

class GroupUpdate(BaseModel):
    id: int
    name: Optional[str]
    company: Optional[str]

class IdolDelete(BaseModel):
    id: int

class GroupDelete(BaseModel):
    id: int
