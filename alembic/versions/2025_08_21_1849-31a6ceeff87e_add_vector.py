"""add vector

Revision ID: 31a6ceeff87e
Revises: 6ee357ebdcb4
Create Date: 2025-08-21 18:49:40.567552

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "31a6ceeff87e"
down_revision = "6ee357ebdcb4"
branch_labels = None
depends_on = None


def upgrade():
    # Добавляем новое векторное поле в movies
    op.execute(
        """
        ALTER TABLE movies
        ADD COLUMN plot_embedding vector(384) NOT NULL;
    """
    )


def downgrade():
    # Удаляем векторное поле
    op.execute(
        """
        ALTER TABLE movies
        DROP COLUMN plot_embedding;
    """
    )
