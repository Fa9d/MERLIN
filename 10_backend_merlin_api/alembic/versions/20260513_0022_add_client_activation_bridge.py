"""add client activation bridge

Revision ID: 20260513_0022
Revises: 20260511_0021
Create Date: 2026-05-13
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260513_0022"
down_revision: Union[str, Sequence[str], None] = "20260511_0021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("clients") as batch_op:
        batch_op.add_column(sa.Column("app_user_id", sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column("activation_token_hash", sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column("activation_token_expires_at", sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column("activation_invited_at", sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column("activation_accepted_at", sa.DateTime(timezone=True), nullable=True))
        batch_op.create_unique_constraint("uq_clients_app_user_id", ["app_user_id"])
        batch_op.create_foreign_key(
            "fk_clients_app_user_id_app_users",
            "app_users",
            ["app_user_id"],
            ["id"],
            ondelete="SET NULL",
        )

    op.create_index("ix_clients_app_user_id", "clients", ["app_user_id"])
    op.create_index("ix_clients_activation_token_hash", "clients", ["activation_token_hash"])


def downgrade() -> None:
    op.drop_index("ix_clients_activation_token_hash", table_name="clients")
    op.drop_index("ix_clients_app_user_id", table_name="clients")

    with op.batch_alter_table("clients") as batch_op:
        batch_op.drop_constraint("fk_clients_app_user_id_app_users", type_="foreignkey")
        batch_op.drop_constraint("uq_clients_app_user_id", type_="unique")
        batch_op.drop_column("activation_accepted_at")
        batch_op.drop_column("activation_invited_at")
        batch_op.drop_column("activation_token_expires_at")
        batch_op.drop_column("activation_token_hash")
        batch_op.drop_column("app_user_id")