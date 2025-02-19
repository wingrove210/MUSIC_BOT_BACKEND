"""Recreate missing revision

Revision ID: ad2b2d31ef81
Revises: b758c2c8eae6
Create Date: 2025-02-19 01:59:28.747292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad2b2d31ef81'
down_revision: Union[str, None] = 'b758c2c8eae6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
