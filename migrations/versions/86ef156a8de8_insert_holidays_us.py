from typing import Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from models.holiday import Holiday
from services.holiday_import import insert_state_holidays, insert_us_holidays


# revision identifiers, used by Alembic.

revision: str = "86ef156a8de8"
down_revision: Union[str, None] = "d123cfe7f7d6"
branch_labels: Union[str, sa.Sequence[str], None] = None
depends_on: Union[str, sa.Sequence[str], None] = None




def upgrade():
    bind = op.get_bind()
    session = Session(bind)

    insert_us_holidays(session)
    insert_state_holidays(session)


def downgrade():
    bind = op.get_bind()
    session = Session(bind)
    session.execute(sa.delete(Holiday))
    session.commit()
