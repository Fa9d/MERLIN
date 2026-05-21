from fastapi import APIRouter, BackgroundTasks, status
from pydantic import BaseModel, EmailStr, Field

from app.services.email import (
    make_organization_lead_admin_email,
    make_organization_lead_confirmation_email,
    send_email,
)

router = APIRouter(prefix="/organization-leads", tags=["organization_leads"])


class OrganizationLeadCreate(BaseModel):
    display_name: str = Field(min_length=1, max_length=200)
    organization_name: str = Field(min_length=1, max_length=240)
    email: EmailStr
    organization_type: str | None = Field(default=None, max_length=120)


class OrganizationLeadResponse(BaseModel):
    message: str


@router.post("", response_model=OrganizationLeadResponse, status_code=status.HTTP_202_ACCEPTED)
def create_organization_lead(
    payload: OrganizationLeadCreate,
    background_tasks: BackgroundTasks,
) -> OrganizationLeadResponse:
    client_html, client_text = make_organization_lead_confirmation_email(
        display_name=payload.display_name,
        organization_name=payload.organization_name,
    )
    background_tasks.add_task(
        send_email,
        to_email=str(payload.email),
        subject="Nous avons bien reçu votre demande IVIA Organisations",
        html_body=client_html,
        text_body=client_text,
        audience="client",
    )

    admin_html, admin_text = make_organization_lead_admin_email(
        display_name=payload.display_name,
        organization_name=payload.organization_name,
        email=str(payload.email),
        organization_type=payload.organization_type,
    )
    background_tasks.add_task(
        send_email,
        to_email="organisations@ivia.ca",
        subject=f"Nouveau lead organisation — {payload.organization_name}",
        html_body=admin_html,
        text_body=admin_text,
        audience="admin",
    )

    return OrganizationLeadResponse(message="Demande organisation reçue.")
