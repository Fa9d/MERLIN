"""add intake request handling fields

Revision ID: 20260511_0019
Revises: 20260507_0018
Create Date: 2026-05-11
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260511_0019"
down_revision: Union[str, Sequence[str], None] = "20260507_0018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_VALID_HANDLING_STATUSES = (
    "new",
    "a_rappeler",
    "contacte",
    "planifie",
    "vigilance",
    "hors_cadre",
    "archive",
)
_CHECK_NAME = "ck_intake_requests_handling_status_code"


def _column_exists(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    with op.batch_alter_table("intake_requests") as batch_op:
        if not _column_exists(inspector, "intake_requests", "handling_status_code"):
            batch_op.add_column(
                sa.Column(
                    "handling_status_code",
                    sa.String(length=32),
                    nullable=False,
                    server_default="new",
                )
            )
        if not _column_exists(inspector, "intake_requests", "handling_notes"):
            batch_op.add_column(sa.Column("handling_notes", sa.Text(), nullable=True))
        if not _column_exists(inspector, "intake_requests", "handled_by_user_id"):
            batch_op.add_column(sa.Column("handled_by_user_id", sa.String(length=36), nullable=True))
        if not _column_exists(inspector, "intake_requests", "handled_at"):
            batch_op.add_column(sa.Column("handled_at", sa.DateTime(timezone=True), nullable=True))

    constraints = {constraint["name"] for constraint in inspector.get_check_constraints("intake_requests")}
    if _CHECK_NAME not in constraints:
        op.create_check_constraint(
            _CHECK_NAME,
            "intake_requests",
            sa.column("handling_status_code").in_(_VALID_HANDLING_STATUSES),
        )

    with op.batch_alter_table("intake_requests") as batch_op:
        batch_op.alter_column("handling_status_code", server_default=None)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    constraints = {constraint["name"] for constraint in inspector.get_check_constraints("intake_requests")}
    if _CHECK_NAME in constraints:
        op.drop_constraint(_CHECK_NAME, "intake_requests", type_="check")

    with op.batch_alter_table("intake_requests") as batch_op:
        if _column_exists(inspector, "intake_requests", "handled_at"):
            batch_op.drop_column("handled_at")
        if _column_exists(inspector, "intake_requests", "handled_by_user_id"):
            batch_op.drop_column("handled_by_user_id")
        if _column_exists(inspector, "intake_requests", "handling_notes"):
            batch_op.drop_column("handling_notes")
        if _column_exists(inspector, "intake_requests", "handling_status_code"):
            batch_op.drop_column("handling_status_code")
