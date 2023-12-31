"""

Revision ID: 22ac833900e2
Revises: 72d081e993a8
Create Date: 2023-12-31 10:08:22.211065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22ac833900e2'
down_revision: Union[str, None] = '72d081e993a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    # Execute a SQL command to update the altitude column
    connection.execute(
        sa.text(
            "UPDATE explained_images SET altitude = REPLACE(altitude, 'm', '') WHERE "
            "altitude LIKE '%m'"
        )
    )
    # change latitude, longitude to floats, altitude to int
    op.execute(
        "ALTER TABLE explained_images ALTER COLUMN latitude TYPE double precision USING (latitude::double precision)")
    op.execute(
        "ALTER TABLE explained_images ALTER COLUMN longitude TYPE double precision USING (longitude::double precision)")
    op.execute(
        "ALTER TABLE explained_images ALTER COLUMN altitude TYPE integer "
        "USING ("
        "altitude::integer)")


def downgrade() -> None:
    # change latitude, longitude to strings, altitude to string
    op.execute(
        "ALTER TABLE explained_images ALTER COLUMN latitude TYPE varchar USING (latitude::text)")
    op.execute(
        "ALTER TABLE explained_images ALTER COLUMN longitude TYPE varchar USING (longitude::text)")
    op.execute(
        "ALTER TABLE explained_images ALTER COLUMN altitude TYPE varchar USING ("
        "altitude::text)")
