from sqlalchemy import select, and_, or_, extract
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List, Optional
from models.holiday import Holiday


async def get_holidays_with_filters(
    db: AsyncSession,
    year: Optional[int] = None,
    month: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    name: Optional[str] = None,
    type: Optional[str] = None,
    state: Optional[str] = None,
    states: Optional[List[str]] = None,
    custom: Optional[bool] = None,
) -> List[Holiday]:
    query = select(Holiday)

    if year:
        query = query.where(extract("year", Holiday.date) == year)

    if month:
        query = query.where(extract("month", Holiday.date) == month)

    if start_date and end_date:
        query = query.where(and_(Holiday.date >= start_date, Holiday.date <= end_date))
    elif start_date:
        query = query.where(Holiday.date >= start_date)
    elif end_date:
        query = query.where(Holiday.date <= end_date)

    if name:
        query = query.where(Holiday.name.ilike(f"%{name}%"))

    if state:
        query = query.where(Holiday.states.contains([state]))

    if states:
        query = query.where(or_(*[Holiday.states.contains([s]) for s in states]))

    if custom is not None:
        query = query.where(Holiday.is_custom == custom)

    if type is not None:
        query = query.where(Holiday.type.ilike(f"%{type}%"))

    result = await db.execute(query)
    return result.scalars().all()
