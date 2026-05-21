"""add booking entitlement consumption

Revision ID: 20260518_0026
Revises: 20260518_0025
Create Date: 2026-05-18
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260518_0026"
down_revision: Union[str, Sequence[str], None] = "20260518_0025"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("booking_slots") as batch_op:
        batch_op.add_column(sa.Column("consumed_entitlement_id", sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column("consumed_entitlement_units", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_booking_slots_consumed_entitlement_id_client_entitlements",
            "client_entitlements",
            ["consumed_entitlement_id"],
            ["id"],
            ondelete="SET NULL",
        )

    op.create_index(
        "ix_booking_slots_consumed_entitlement_id",
        "booking_slots",
        ["consumed_entitlement_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_booking_slots_consumed_entitlement_id", table_name="booking_slots")
    with op.batch_alter_table("booking_slots") as batch_op:
        batch_op.drop_constraint(
            "fk_booking_slots_consumed_entitlement_id_client_entitlements",
            type_="foreignkey",
        )
        batch_op.drop_column("consumed_entitlement_units")
        batch_op.drop_column("consumed_entitlement_id")