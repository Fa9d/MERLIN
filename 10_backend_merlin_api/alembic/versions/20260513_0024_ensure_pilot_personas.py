"""ensure pilot personas

Revision ID: 20260513_0024
Revises: 20260513_0023
Create Date: 2026-05-13
"""
import hashlib
import json
import secrets
from datetime import datetime, timezone
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


revision: str = "20260513_0024"
down_revision: Union[str, Sequence[str], None] = "20260513_0023"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PERSONAS = [
    {
        "email": "pilote.aelis@ivia.quebec",
        "display_name": "Aelis",
        "title_line": "Accompagnatrice - corps et silence",
        "intro_text": "Aelis tient un espace ou le corps a la parole, sans chercher a nommer trop vite.",
        "bio": "Aelis travaille avec ce que le corps tient sans le dire, avec une presence lente et attentive.",
        "presentation_audio_url": "/assets/voix_pilote/voix_01_corps_silence.mp3",
        "domaines": ["sante", "anxiete", "trauma"],
        "approches": ["psychocorporel", "ecoute_active"],
        "abstract_palette": "vert_sauge",
        "abstract_texture": "souffle",
        "abstract_motif": "cercle",
        "listening_modality": "corps_silence",
        "pilot_persona_label": "voix_pilote_01",
    },
    {
        "email": "pilote.nael@ivia.quebec",
        "display_name": "Nael",
        "title_line": "Accompagnateur - mots et structure",
        "intro_text": "Nael travaille avec les mots comme appui pour clarifier ce qui s'embrouille.",
        "bio": "Nael accompagne les periodes ou l'on ne sait plus comment s'organiser ni se raconter.",
        "presentation_audio_url": "/assets/voix_pilote/voix_02_mots_structure.mp3",
        "domaines": ["travail", "transition", "identite"],
        "approches": ["ecoute_active", "outils_concrets"],
        "abstract_palette": "ardoise",
        "abstract_texture": "grain_papier",
        "abstract_motif": "ligne_horizon",
        "listening_modality": "mots_structure",
        "pilot_persona_label": "voix_pilote_02",
    },
    {
        "email": "pilote.seve@ivia.quebec",
        "display_name": "Seve",
        "title_line": "Accompagnatrice - frequence et vibration",
        "intro_text": "Seve accompagne ceux qui sentent que quelque chose en eux cherche a se reequilibrer.",
        "bio": "Seve travaille a l'endroit ou le corps et l'elan se rejoignent.",
        "presentation_audio_url": "/assets/voix_pilote/voix_03_frequence_vibration.mp3",
        "domaines": ["identite", "sante", "anxiete"],
        "approches": ["psychocorporel", "spirituel"],
        "abstract_palette": "ambre",
        "abstract_texture": "ondulation",
        "abstract_motif": "vague",
        "listening_modality": "frequence_vibration",
        "pilot_persona_label": "voix_pilote_03",
    },
    {
        "email": "pilote.telma@ivia.quebec",
        "display_name": "Telma",
        "title_line": "Accompagnatrice - contemplation et ancrage",
        "intro_text": "Telma cree un espace de stabilite pour ceux qui traversent une perte ou un passage.",
        "bio": "Telma est disponible pour ce qui ne peut pas encore etre dit.",
        "presentation_audio_url": "/assets/voix_pilote/voix_04_contemplation_ancrage.mp3",
        "domaines": ["anxiete", "deuil", "transition"],
        "approches": ["spirituel", "ecoute_active"],
        "abstract_palette": "lin",
        "abstract_texture": "veinure",
        "abstract_motif": "feuille",
        "listening_modality": "contemplation_ancrage",
        "pilot_persona_label": "voix_pilote_04",
    },
    {
        "email": "pilote.nori@ivia.quebec",
        "display_name": "Nori",
        "title_line": "Accompagnateur - energie et mouvement",
        "intro_text": "Nori accompagne les periodes de changement ou l'energie manque ou s'emballe.",
        "bio": "Nori travaille avec ce qui circule ou ce qui est bloque.",
        "presentation_audio_url": "/assets/voix_pilote/voix_05_energie_mouvement.mp3",
        "domaines": ["travail", "relation", "transition"],
        "approches": ["outils_concrets", "approche_systemique"],
        "abstract_palette": "ocre_doux",
        "abstract_texture": "halo",
        "abstract_motif": "spirale_ouverte",
        "listening_modality": "energie_mouvement",
        "pilot_persona_label": "voix_pilote_05",
    },
    {
        "email": "pilote.solene@ivia.quebec",
        "display_name": "Solene",
        "title_line": "Accompagnatrice - deuil et transition",
        "intro_text": "Solene est presente aux passages difficiles, sans chercher a consoler trop vite.",
        "bio": "Solene accompagne ce qui est encore en train de se traverser.",
        "presentation_audio_url": "/assets/voix_pilote/voix_06_deuil_transition.mp3",
        "domaines": ["deuil", "famille", "transition"],
        "approches": ["ecoute_active", "narratif"],
        "abstract_palette": "argile",
        "abstract_texture": "trame",
        "abstract_motif": "pierre",
        "listening_modality": "deuil_transition",
        "pilot_persona_label": "voix_pilote_06",
    },
]

SCHEDULE_BLOCKS = [
    (0, "09:00:00", "12:00:00"),
    (2, "13:00:00", "16:00:00"),
    (4, "09:00:00", "12:00:00"),
]


def _hash_password_scrypt(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt:{salt.hex()}:{digest.hex()}"


def _ensure_schedule(bind, user_id: str, now: datetime) -> None:
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


def upgrade() -> None:
    bind = op.get_bind()

    # Add columns that were lost from missing migrations 0019/0020
    # Use ADD COLUMN IF NOT EXISTS (PostgreSQL 9.6+) — safe inside a transaction
    extra_cols = [
        ("abstract_palette",   "VARCHAR(50)"),
        ("abstract_texture",   "VARCHAR(50)"),
        ("abstract_motif",     "VARCHAR(50)"),
        ("listening_modality", "VARCHAR(100)"),
        ("pilot_persona_label","VARCHAR(50)"),
    ]
    for col_name, col_type in extra_cols:
        bind.execute(
            sa.text(
                f"ALTER TABLE practitioner_profiles ADD COLUMN IF NOT EXISTS {col_name} {col_type}"
            )
        )

    now = datetime.now(timezone.utc)

    for persona in PERSONAS:
        user_id = bind.execute(
            sa.text("SELECT id FROM app_users WHERE email = :email"),
            {"email": persona["email"]},
        ).scalar_one_or_none()

        if user_id is None:
            user_id = str(uuid4())
            bind.execute(
                sa.text(
                    """
                    INSERT INTO app_users (
                        id, email, password_hash, display_name,
                        title_line, intro_text, presentation_audio_url,
                        spoken_languages, available_channels,
                        is_publicly_listed, role, record_status,
                        email_verified, created_at, updated_at
                    ) VALUES (
                        :id, :email, :password_hash, :display_name,
                        :title_line, :intro_text, :presentation_audio_url,
                        :spoken_languages, :available_channels,
                        true, 'practitioner', 'active', true, :created_at, :updated_at
                    )
                    """
                ),
                {
                    "id": user_id,
                    "email": persona["email"],
                    "password_hash": _hash_password_scrypt(secrets.token_urlsafe(32)),
                    "display_name": persona["display_name"],
                    "title_line": persona["title_line"],
                    "intro_text": persona["intro_text"],
                    "presentation_audio_url": persona["presentation_audio_url"],
                    "spoken_languages": json.dumps(["fr"]),
                    "available_channels": json.dumps(["video", "audio"]),
                    "created_at": now,
                    "updated_at": now,
                },
            )

        existing_profile_id = bind.execute(
            sa.text("SELECT id FROM practitioner_profiles WHERE user_id = :user_id"),
            {"user_id": user_id},
        ).scalar_one_or_none()
        if existing_profile_id is None:
            bind.execute(
                sa.text(
                    """
                    INSERT INTO practitioner_profiles (
                        user_id, display_name, bio,
                        modalites, langues, approches,
                        public_visible, accepting_clients,
                        title_line, intro_text, presentation_audio_url,
                        domaines, disponibilites, tarif_horaire_cents, actif,
                        abstract_palette, abstract_texture, abstract_motif,
                        listening_modality, pilot_persona_label,
                        created_at, updated_at
                    ) VALUES (
                        :user_id, :display_name, :bio,
                        :modalites, :langues, :approches,
                        true, true,
                        :title_line, :intro_text, :presentation_audio_url,
                        :domaines, :disponibilites, 8000, true,
                        :abstract_palette, :abstract_texture, :abstract_motif,
                        :listening_modality, :pilot_persona_label,
                        :created_at, :updated_at
                    )
                    """
                ),
                {
                    "user_id": user_id,
                    "display_name": persona["display_name"],
                    "bio": persona["bio"],
                    "modalites": json.dumps([persona["listening_modality"]]),
                    "langues": json.dumps(["fr"]),
                    "approches": json.dumps(persona["approches"]),
                    "title_line": persona["title_line"],
                    "intro_text": persona["intro_text"],
                    "presentation_audio_url": persona["presentation_audio_url"],
                    "domaines": json.dumps(persona["domaines"]),
                    "disponibilites": json.dumps(["matin", "soir"]),
                    "abstract_palette": persona["abstract_palette"],
                    "abstract_texture": persona["abstract_texture"],
                    "abstract_motif": persona["abstract_motif"],
                    "listening_modality": persona["listening_modality"],
                    "pilot_persona_label": persona["pilot_persona_label"],
                    "created_at": now,
                    "updated_at": now,
                },
            )

        _ensure_schedule(bind, user_id, now)


def downgrade() -> None:
    pass