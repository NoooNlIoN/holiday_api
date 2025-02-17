from datetime import date
from pydantic import BaseModel
from typing import List, Optional


class HolidayBase(BaseModel):
    name: str
    date: date
    states: Optional[List[str]] = None


class HolidayCreate(HolidayBase):
    pass


class HolidayResponse(HolidayBase):
    id: int
    is_custom: bool


class HolidayUpdate(BaseModel):
    name: Optional[str] = None
    states: Optional[List[str]] = None
