from typing import Optional
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


def get_appointment(db: Session, appointment_id: int) -> Optional[Appointment]:
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_appointments(db: Session, skip: int = 0, limit: int = 100) -> list[Appointment]:
    return db.query(Appointment).offset(skip).limit(limit).all()


def create_appointment(db: Session, data: AppointmentCreate) -> Appointment:
    appointment = Appointment(**data.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def update_appointment(
    db: Session, appointment_id: int, data: AppointmentUpdate
) -> Optional[Appointment]:
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(appointment, field, value)
    db.commit()
    db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment_id: int) -> bool:
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        return False
    db.delete(appointment)
    db.commit()
    return True
