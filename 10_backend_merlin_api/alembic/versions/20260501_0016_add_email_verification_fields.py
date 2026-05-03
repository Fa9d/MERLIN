"""add email verification fields to app_users

Revision ID: 20260501_0016
Revises: 20260501_0015
Create Date: 2026-05-01
"""
from alembic import op
import sqlalchemy as sa

revision = "20260501_0016"
down_revision = "20260501_0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "app_users",
        sa.Column("email_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "app_users",
        sa.Column("email_verification_token", sa.String(128), nullable=True),
    )
    op.add_column(
        "app_users",
        sa.Column("token_expires_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("app_users", "token_expires_at")
    op.drop_column("app_users", "email_verification_token")
    op.drop_column("app_users", "email_verified")
