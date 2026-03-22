import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Query, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models.application import ApplicationStatus, Application
from app.models.user import User
from app.schemas.jobs import ApplicationCreate, ApplicationUpdate
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("/", tags=["jobs"])
def list_applications(
        current_user: Annotated[User, Depends(get_current_user)],
        status: ApplicationStatus | None = Query(None),
        company: str | None = Query(None),
        sort: str | None = Query("applied_date"),
        session: Session = Depends(get_session),
):
    query = select(Application).where(Application.user_id == current_user.id)
    print(query)
    if status:
        query = query.where(Application.status == status)
    if company:
        query = query.where(Application.company.ilike(f"%{company}%"))
    return session.exec(query).all()


@router.get("/{id}", tags=["jobs"])
def get_application(
        id: uuid.UUID,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session)
):
    query = select(Application).where(Application.user_id == current_user.id).where(Application.id == id)
    return session.exec(query).one_or_none()


@router.post("/", tags=["jobs"])
def create_application(
        data: ApplicationCreate,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session)
):
    application = Application(**data.model_dump(), user_id=current_user.id)
    session.add(application)
    session.commit()
    session.refresh(application)
    return application


@router.patch("/{id}", tags=["jobs"])
def update_application(
        id: uuid.UUID,
        data: ApplicationUpdate,
        session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
):
    application = session.get(Application, id)
    if not application or application.user_id != current_user.id:
        raise HTTPException(status_code=404)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(application, field, value)
    session.add(application)
    session.commit()
    session.refresh(application)
    return application
