"""seed pilot practitioner schedules

Revision ID: 20260513_0023
Revises: 20260513_0022
Create Date: 2026-05-13
"""
from datetime import datetime, timezone
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


revision: str = "20260513_0023"
down_revision: Union[str, Sequence[str], None] = "20260513_0022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PILOT_EMAILS = [
    "pilote.aelis@ivia.quebec",
    "pilote.nael@ivia.quebec",
    "pilote.seve@ivia.quebec",
    "pilote.telma@ivia.quebec",
    "pilote.nori@ivia.quebec",
    "pilote.solene@ivia.quebec",
]

SCHEDULE_BLOCKS = [
    (0, "09:00:00", "12:00:00"),
    (2, "13:00:00", "16:00:00"),
    (4, "09:00:00", "12:00:00"),
]


def upgrade() -> None:
    bind = op.get_bind()
    now = datetime.now(timezone.utc)

    for email in PILOT_EMAILS:
        user_id = bind.execute(
            sa.text("SELECT id FROM app_users WHERE email = :email"),
            {"email": email},
        ).scalar_one_or_none()
        if user_id is None:
            continue

        for day_of_week, start_time, end_time in SCHEDULE_BLOCKS:
            existing_id = bind.execute(
                sa.text(
                    """
                    SELECT id FROM practitioner_schedules
                    WHERE praticien_id = :praticien_id
                      AND day_of_week = :day_of_week
                      AND start_time = CAST(:start_time AS time)
                      AND end_time = CAST(:end_time AS time)
                      AND session_type = 'standard'
                    """
                ),
                {
                    "praticien_id": user_id,
                    "day_of_week": day_of_week,
                    "start_time": start_time,
                    "end_time": end_time,
                },
            ).scalar_one_or_none()
            if existing_id is not None:
                continue

            bind.execute(
                sa.text(
                    """
                    INSERT INTO practitioner_schedules (
                        id, praticien_id, day_of_week, start_time, end_time,
                        session_duration_minutes, buffer_minutes, session_type,
                        valid_from, valid_until, is_active, created_at, updated_at
                    ) VALUES (
                        :id, :praticien_id, :day_of_week,
                        CAST(:start_time AS time), CAST(:end_time AS time),
                        60, 15, 'standard', NULL, NULL, true, :created_at, :updated_at
                    )
                    """
                ),
                {
                    "id": str(uuid4()),
                    "praticien_id": user_id,
                    "day_of_week": day_of_week,
                    "start_time": start_time,
                    "end_time": end_time,
                    "created_at": now,
                    "updated_at": now,
                },
            )


def downgrade() -> None:
    bind = op.get_bind()

    for email in PILOT_EMAILS:
        user_id = bind.execute(
            sa.text("SELECT id FROM app_users WHERE email = :email"),
            {"email": email},
        ).scalar_one_or_none()
        if user_id is None:
            continue

        for day_of_week, start_time, end_time in SCHEDULE_BLOCKS:
            bind.execute(
                sa.text(
                    """
                    DELETE FROM practitioner_schedules
                    WHERE praticien_id = :praticien_id
                      AND day_of_week = :day_of_week
                      AND start_time = CAST(:start_time AS time)
                      AND end_time = CAST(:end_time AS time)
                      AND session_type = 'standard'
                    """
                ),
                {
                    "praticien_id": user_id,
                    "day_of_week": day_of_week,
                    "start_time": start_time,
                    "end_time": end_time,
                },
            )