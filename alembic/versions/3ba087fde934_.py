"""

Revision ID: 3ba087fde934
Revises: e5cd4f2024a3
Create Date: 2024-01-01 10:51:06.903944

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ba087fde934'
down_revision: Union[str, None] = 'e5cd4f2024a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add 'echo_id' column to 'explained_image' table
    op.add_column('explained_images', sa.Column('echo_id', sa.UUID(as_uuid=True),
                                                nullable=True))
    op.create_foreign_key('fk_echo_explained_image', 'explained_images', 'echo',
                          ['echo_id'], ['id'])


def downgrade():
    # Remove the foreign key constraint
    op.drop_constraint('fk_echo_explained_image', 'explained_images',
                       type_='foreignkey')

    # Remove 'echo_id' column from 'explained_image'
    op.drop_column('explained_images', 'echo_id')

    # Drop the 'echo' table
    op.drop_table('echo')
