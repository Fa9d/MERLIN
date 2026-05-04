"""add RequestChannelCode enum constraint on intake_requests.request_channel_code

Revision ID: 20260504_0017
Revises: 20260501_0016
Create Date: 2026-05-04
"""
from alembic import op
import sqlalchemy as sa

revision = "20260504_0017"
down_revision = "20260501_0016"
branch_labels = None
depends_on = None

_VALID_VALUES = ("web_form", "phone", "email", "referral", "other")
_CHECK_NAME = "ck_intake_requests_request_channel_code"


def upgrade() -> None:
    op.alter_column(
        "intake_requests",
        "request_channel_code",
        existing_type=sa.String(32),
        type_=sa.String(32),
        existing_nullable=False,
        nullable=False,
    )
    op.create_check_constraint(
        _CHECK_NAME,
        "intake_requests",
        sa.column("request_channel_code").in_(_VALID_VALUES),
    )


def downgrade() -> None:
    op.drop_constraint(_CHECK_NAME, "intake_requests", type_="check")
