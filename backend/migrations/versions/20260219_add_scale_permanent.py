"""Add permanent 'scale' column to farms

Revision ID: add_scale_permanent
Revises: 62f4ee7dc877
Create Date: 2026-02-19 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_scale_permanent'
down_revision = '62f4ee7dc877'
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ Add the column (nullable temporarily)
    op.add_column('farms', sa.Column('scale', sa.String(), nullable=True))

    # 2️⃣ Populate based on existing size JSON
    op.execute(
        """
        UPDATE farms
        SET scale =
            CASE
                WHEN size IS NOT NULL AND (size->>'value')::float < 5 THEN 'small'
                WHEN size IS NOT NULL AND (size->>'value')::float < 20 THEN 'medium'
                ELSE 'large'
            END;
        """
    )

    # 3️⃣ Make column NOT NULL for production
    op.alter_column('farms', 'scale', nullable=False)

    # 4️⃣ Optional: add index if needed
    op.create_index('idx_farms_scale', 'farms', ['scale'])


def downgrade():
    # Drop the column if rolling back
    op.drop_index('idx_farms_scale', table_name='farms')
    op.drop_column('farms', 'scale')

