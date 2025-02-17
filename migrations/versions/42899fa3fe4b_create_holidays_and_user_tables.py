"""create holidays and user tables

Revision ID: 42899fa3fe4b
Revises: c31d3b21140f
Create Date: 2025-02-13 11:22:21.870563

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = "42899fa3fe4b"
down_revision: Union[str, None] = "c31d3b21140f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table(
        "holidays",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False, unique=False),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("states", sa.ARRAY(sa.String), nullable=True),
        sa.Column("is_custom", sa.Boolean, default=False),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("jwt", sa.String),
    )


def downgrade() -> None:
    op.drop_table("holidays")
    op.drop_table("users")

