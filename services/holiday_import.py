import holidays
from sqlalchemy.orm import Session
from models.holiday import Holiday
from sqlalchemy.dialects.postgresql import insert
from us import states

def insert_us_holidays(session: Session):
    us_holidays = holidays.US(years=range(2024, 2030))
    holidays_list = []

    for date, name in us_holidays.items():
        holidays_list.append({
            "date": date,
            "name": name,
            "states": None,
            "type": "national",
            "is_custom": False
        })

    session.execute(insert(Holiday).values(holidays_list).on_conflict_do_nothing())
    session.commit()


def insert_state_holidays(session: Session):
    state_list = [state.abbr for state in states.STATES]
    holidays_list = []

    for state in state_list:
        state_holidays = holidays.US(years=range(2024, 2030), state=state)
        for date, name in state_holidays.items():
            holidays_list.append({
                "date": date,
                "name": name,
                "states": [state],
                "type": "state",
                "is_custom": False
            })

    session.execute(insert(Holiday).values(holidays_list).on_conflict_do_nothing())
    session.commit()
