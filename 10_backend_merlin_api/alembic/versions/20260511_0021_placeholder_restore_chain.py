"""placeholder revision to restore missing alembic chain

Revision ID: 20260511_0021
Revises: 20260507_0018
Create Date: 2026-05-11

This revision was missing from the repository history. It is intentionally
no-op so existing databases already stamped/applied through 20260513_0022+
can continue migrating safely.
"""

from typing import Sequence, Union


revision: str = "20260511_0021"
down_revision: Union[str, Sequence[str], None] = "20260507_0018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    return None


def downgrade() -> None:
    return None