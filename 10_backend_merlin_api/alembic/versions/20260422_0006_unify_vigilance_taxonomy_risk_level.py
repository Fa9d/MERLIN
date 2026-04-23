"""unify vigilance taxonomy to risk level code

Revision ID: 20260422_0006
Revises: 20260422_0005
Create Date: 2026-04-22 16:25:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260422_0006"
down_revision: Union[str, Sequence[str], None] = "20260422_0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


OLD_VIGILANCE_ENUM = sa.Enum(
    "non_urgent",
    "watch",
    "priority",
    "urgent",
    name="perceivedurgencycode",
    native_enum=False,
)

NEW_VIGILANCE_ENUM = sa.Enum(
    "non_urgent",
    "watch",
    "priority",
    "urgent",
    name="risklevelcode",
    native_enum=False,
)


def upgrade() -> None:
    op.alter_column(
        "intake_requests",
        "perceived_urgency_code",
        existing_type=OLD_VIGILANCE_ENUM,
        type_=NEW_VIGILANCE_ENUM,
        existing_nullable=False,
    )
    op.alter_column(
        "session_notes",
        "vigilance_level_code",
        existing_type=OLD_VIGILANCE_ENUM,
        type_=NEW_VIGILANCE_ENUM,
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "session_notes",
        "vigilance_level_code",
        existing_type=NEW_VIGILANCE_ENUM,
        type_=OLD_VIGILANCE_ENUM,
        existing_nullable=False,
    )
    op.alter_column(
        "intake_requests",
        "perceived_urgency_code",
        existing_type=NEW_VIGILANCE_ENUM,
        type_=OLD_VIGILANCE_ENUM,
        existing_nullable=False,
    )
