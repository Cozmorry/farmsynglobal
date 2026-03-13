"""create farms module tables with robust JSON conversion and mixed units handling

Revision ID: 62f4ee7dc877
Revises: 665bb216e9af
Create Date: 2026-02-17 09:01:09.146038
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62f4ee7dc877'
down_revision: Union[str, Sequence[str], None] = '665bb216e9af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # --------------------------------------------------
    # Add farm_type column safely (existing rows get 'crop' temporarily)
    # --------------------------------------------------
    op.add_column('farms', sa.Column(
        'farm_type',
        sa.Enum('crop', 'livestock', 'poultry', 'aquaculture', 'mixed', name='farm_type_enum'),
        nullable=False,
        server_default='crop'  # temporary default for existing rows
    ))
    # Remove the server default so future inserts must specify farm_type
    op.alter_column('farms', 'farm_type', server_default=None)

    # --------------------------------------------------
    # SAFELY CONVERT farms.size → JSON (preserve original units)
    # Handles values like "10 acres", "5 ha", "12"
    # --------------------------------------------------
    op.execute(
        """
        ALTER TABLE farms
        ALTER COLUMN size TYPE JSON
        USING (
            CASE
                WHEN size IS NULL OR trim(size) = '' THEN NULL
                WHEN size ~* 'ac' THEN
                    json_build_object(
                        'value',
                        regexp_replace(size, '[^0-9\\.]', '', 'g')::float,
                        'unit',
                        'ac'
                    )
                WHEN size ~* 'ha' THEN
                    json_build_object(
                        'value',
                        regexp_replace(size, '[^0-9\\.]', '', 'g')::float,
                        'unit',
                        'ha'
                    )
                WHEN size ~* 'sqm|m2' THEN
                    json_build_object(
                        'value',
                        round((regexp_replace(size, '[^0-9\\.]', '', 'g')::float / 10000)::numeric, 2),
                        'unit',
                        'ha'
                    )
                ELSE
                    -- default unknown units to ha
                    json_build_object(
                        'value',
                        regexp_replace(size, '[^0-9\\.]', '', 'g')::float,
                        'unit',
                        'ha'
                    )
            END
        )
        """
    )

    # --------------------------------------------------
    # SAFELY CONVERT blocks.area → JSON (rounded 2 decimals)
    # --------------------------------------------------
    op.execute(
        """
        ALTER TABLE blocks
        ALTER COLUMN area TYPE JSON
        USING (
            CASE
                WHEN area IS NULL THEN NULL
                ELSE json_build_object(
                    'value', round(area::numeric, 2),
                    'unit', 'ha'
                )
            END
        )
        """
    )

    # --------------------------------------------------
    # SAFELY CONVERT greenhouses.area → JSON (rounded 2 decimals)
    # --------------------------------------------------
    op.execute(
        """
        ALTER TABLE greenhouses
        ALTER COLUMN area TYPE JSON
        USING (
            CASE
                WHEN area IS NULL THEN NULL
                ELSE json_build_object(
                    'value', round(area::numeric, 2),
                    'unit', 'ha'
                )
            END
        )
        """
    )

    # --------------------------------------------------
    # SAFELY CONVERT ponds.size → JSON (rounded 2 decimals)
    # --------------------------------------------------
    op.execute(
        """
        ALTER TABLE ponds
        ALTER COLUMN size TYPE JSON
        USING (
            CASE
                WHEN size IS NULL THEN NULL
                ELSE json_build_object(
                    'value', round(size::numeric, 2),
                    'unit', 'ha'
                )
            END
        )
        """
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Drop farm_type column
    op.drop_column('farms', 'farm_type')

    # Convert ponds.size JSON → DOUBLE safely
    op.execute(
        """
        ALTER TABLE ponds
        ALTER COLUMN size TYPE DOUBLE PRECISION
        USING (
            CASE
                WHEN size IS NULL THEN NULL
                ELSE (size->>'value')::float
            END
        )
        """
    )

    # Convert greenhouses.area JSON → DOUBLE safely
    op.execute(
        """
        ALTER TABLE greenhouses
        ALTER COLUMN area TYPE DOUBLE PRECISION
        USING (
            CASE
                WHEN area IS NULL THEN NULL
                ELSE (area->>'value')::float
            END
        )
        """
    )

    # Convert blocks.area JSON → DOUBLE safely
    op.execute(
        """
        ALTER TABLE blocks
        ALTER COLUMN area TYPE DOUBLE PRECISION
        USING (
            CASE
                WHEN area IS NULL THEN NULL
                ELSE (area->>'value')::float
            END
        )
        """
    )

    # Convert farms.size JSON → TEXT safely (default to 'ha' if unit unknown)
    op.execute(
        """
        ALTER TABLE farms
        ALTER COLUMN size TYPE VARCHAR
        USING (
            CASE
                WHEN size IS NULL THEN NULL
                ELSE (size->>'value') || ' ' || COALESCE(size->>'unit','ha')
            END
        )
        """
    )
