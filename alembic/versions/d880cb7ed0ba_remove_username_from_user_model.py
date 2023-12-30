"""remove username from user model

Revision ID: d880cb7ed0ba
Revises: 93533e12afae
Create Date: 2023-12-30 10:51:32.957857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd880cb7ed0ba'
down_revision: Union[str, None] = '93533e12afae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'username')


def downgrade() -> None:
    op.add_column('users', sa.Column('username', sa.String(length=255)))
