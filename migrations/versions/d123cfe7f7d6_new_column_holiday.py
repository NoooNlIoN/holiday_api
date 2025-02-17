"""new column holiday

Revision ID: d123cfe7f7d6
Revises: 42899fa3fe4b
Create Date: 2025-02-13 14:49:35.727700

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d123cfe7f7d6"
down_revision: Union[str, None] = "42899fa3fe4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "holidays",
        sa.Column("type", sa.String, nullable=True),
    )


def downgrade() -> None:
    op.drop_column(
        "holidays",
        "type",
    )
