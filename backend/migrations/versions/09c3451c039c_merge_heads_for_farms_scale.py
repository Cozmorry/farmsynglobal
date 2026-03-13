"""merge heads for farms scale

Revision ID: 09c3451c039c
Revises: 075aec5f0113, add_scale_permanent
Create Date: 2026-02-19 22:46:24.371613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09c3451c039c'
down_revision: Union[str, Sequence[str], None] = ('075aec5f0113', 'add_scale_permanent')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'scale' only if it does not exist
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name='farms' AND column_name='scale'
        ) THEN
            ALTER TABLE farms ADD COLUMN scale VARCHAR;
        END IF;
    END
    $$;
    """)

    # Populate 'scale' based on 'size'
    op.execute("""
    UPDATE farms
    SET scale =
        CASE
            WHEN size IS NOT NULL AND (size->>'value')::float < 5 THEN 'small'
            WHEN size IS NOT NULL AND (size->>'value')::float < 20 THEN 'medium'
            ELSE 'large'
        END;
    """)

def downgrade() -> None:
    op.execute("ALTER TABLE farms DROP COLUMN IF EXISTS scale;")