"""add vector

Revision ID: 6ee357ebdcb4
Revises: 61d8f735fe4e
Create Date: 2025-08-21 18:39:08.247543

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6ee357ebdcb4"
down_revision = "61d8f735fe4e"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE movies 
        ALTER COLUMN plot TYPE vector(384) USING plot::vector(384)
    """
    )


def downgrade():
    op.execute(
        """
        ALTER TABLE movies 
        ALTER COLUMN plot TYPE VARCHAR USING plot::text
    """
    )
