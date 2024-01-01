"""direction is nullable

Revision ID: e5cd4f2024a3
Revises: 22ac833900e2
Create Date: 2023-12-31 11:59:43.081616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5cd4f2024a3'
down_revision: Union[str, None] = '22ac833900e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        table_name='explained_images',
        column_name='direction',
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        table_name='explained_images',
        column_name='direction',
        nullable=False,
    )
