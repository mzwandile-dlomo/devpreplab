"""Drop username column from users table

Revision ID: 5b3f1e9c2b7c
Revises: 21680a9b721f
Create Date: 2025-11-19 16:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5b3f1e9c2b7c"
down_revision: Union[str, None] = "21680a9b721f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop username-related index if it exists, then the column
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_index("ix_users_username")
        batch_op.drop_column("username")


def downgrade() -> None:
    # Recreate username column and index on downgrade
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("username", sa.String(), nullable=False))
        batch_op.create_index("ix_users_username", ["username"], unique=True)
