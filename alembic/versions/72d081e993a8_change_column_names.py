"""change column names

Revision ID: 72d081e993a8
Revises: d880cb7ed0ba
Create Date: 2023-12-31 09:31:32.786190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72d081e993a8'
down_revision: Union[str, None] = 'd880cb7ed0ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('explained_images', 'comment', new_column_name='title')
    op.alter_column('explained_images', 'ai_comment', new_column_name='additional_comment')
    op.alter_column('explained_images', 'ai_comment_vector', new_column_name='additional_comment_vector')


def downgrade() -> None:
    op.alter_column('explained_images', 'title', new_column_name='comment')
    op.alter_column('explained_images', 'additional_comment', new_column_name='ai_comment')
    op.alter_column('explained_images', 'additional_comment_vector', new_column_name='ai_comment_vector')
