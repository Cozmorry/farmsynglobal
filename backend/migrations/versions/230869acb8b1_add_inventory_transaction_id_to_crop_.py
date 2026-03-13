"""add inventory_transaction_id to crop activities

Revision ID: 230869acb8b1
Revises: f259a8ce7afe
Create Date: 2026-01-10 17:52:07.870241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '230869acb8b1'
down_revision: Union[str, Sequence[str], None] = 'f259a8ce7afe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Chemical applications
    op.add_column(
        "chemical_applications",
        sa.Column("inventory_transaction_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_chemical_inventory_transaction",
        "chemical_applications",
        "inventory_transactions",
        ["inventory_transaction_id"],
        ["id"],
    )

    # Fertilizer applications
    op.add_column(
        "fertilizer_applications",
        sa.Column("inventory_transaction_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_fertilizer_inventory_transaction",
        "fertilizer_applications",
        "inventory_transactions",
        ["inventory_transaction_id"],
        ["id"],
    )

    # Soil amendments
    op.add_column(
        "soil_amendments",
        sa.Column("inventory_transaction_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_soil_inventory_transaction",
        "soil_amendments",
        "inventory_transactions",
        ["inventory_transaction_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_soil_inventory_transaction",
        "soil_amendments",
        type_="foreignkey",
    )
    op.drop_column("soil_amendments", "inventory_transaction_id")

    op.drop_constraint(
        "fk_fertilizer_inventory_transaction",
        "fertilizer_applications",
        type_="foreignkey",
    )
    op.drop_column("fertilizer_applications", "inventory_transaction_id")

    op.drop_constraint(
        "fk_chemical_inventory_transaction",
        "chemical_applications",
        type_="foreignkey",
    )
    op.drop_column("chemical_applications", "inventory_transaction_id")

