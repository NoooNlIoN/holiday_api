from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List, Optional
from core.security import get_current_user
from models.holiday import Holiday
from schemas.holiday import HolidayCreate, HolidayResponse, HolidayUpdate
from core.db import get_db

from filters.holiday import get_holidays_with_filters


from models.user import User


router = APIRouter(prefix="/holidays")


@router.get("/", response_model=List[HolidayResponse])
async def read_holidays(
    year: Optional[int] = None,
    month: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    name: Optional[str] = None,
    state: Optional[str] = None,
    states: Optional[List[str]] = Query(None),
    custom: Optional[bool] = None,
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query_params = {
        "year": year,
        "month": month,
        "start_date": start_date,
        "end_date": end_date,
        "name": name,
        "state": state,
        "states": states,
        "custom": custom,
        "type": type,
    }
    if all(value is None for value in query_params.values()):
        raise HTTPException(
            status_code=404, detail="You must specify at least one parameter"
        )

    filtered_holidays = await get_holidays_with_filters(db, **query_params)

    return filtered_holidays


@router.post("/", response_model=HolidayResponse)
async def create_holiday(
    holiday: HolidayCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_holiday = Holiday(**holiday.dict(), is_custom=True)
    db.add(db_holiday)
    await db.commit()
    await db.refresh(db_holiday)
    return db_holiday


@router.put("/{holiday_id}", response_model=HolidayResponse)
async def update_holiday(
    holiday_id: int,
    holiday: HolidayUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    db_holiday = await db.get(Holiday, holiday_id)
    if not db_holiday or not db_holiday.is_custom:
        raise HTTPException(status_code=404, detail="Holiday not found or not editable or you have no permission")

    for key, value in holiday.dict(exclude_unset=True).items():
        setattr(db_holiday, key, value)
    await db.commit()
    await db.refresh(db_holiday)
    return db_holiday


@router.delete("/{holiday_id}")
async def delete_holiday(
    holiday_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_holiday = await db.get(Holiday, holiday_id)
    if not db_holiday or not db_holiday.is_custom:
        raise HTTPException(status_code=404, detail="Holiday not found or not editable")

    await db.delete(db_holiday)
    await db.commit()
    return {"message": "Holiday deleted"}
