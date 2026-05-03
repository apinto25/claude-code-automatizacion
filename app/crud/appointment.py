from typing import Optional
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


def get_appointment(db: Session, appointment_id: int) -> Optional[Appointment]:
    """Fetch a single appointment by its primary key.

    Args:
        db: Active SQLAlchemy database session.
        appointment_id: Primary key of the appointment to retrieve.

    Returns:
        The matching ``Appointment`` instance, or ``None`` if not found.
    """
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_appointments(db: Session, skip: int = 0, limit: int = 100) -> list[Appointment]:
    """Return a paginated list of all appointments.

    Args:
        db: Active SQLAlchemy database session.
        skip: Number of records to skip (offset). Defaults to 0.
        limit: Maximum number of records to return. Defaults to 100.

    Returns:
        A list of ``Appointment`` instances, possibly empty.
    """
    return db.query(Appointment).offset(skip).limit(limit).all()


def create_appointment(db: Session, data: AppointmentCreate) -> Appointment:
    """Persist a new appointment to the database.

    Args:
        db: Active SQLAlchemy database session.
        data: Validated schema containing the fields for the new appointment.

    Returns:
        The newly created ``Appointment`` instance with its assigned ``id``
        and auto-populated ``created_at`` timestamp.
    """
    appointment = Appointment(**data.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def update_appointment(
    db: Session, appointment_id: int, data: AppointmentUpdate
) -> Optional[Appointment]:
    """Apply a partial update to an existing appointment.

    Only fields explicitly provided in ``data`` are written; omitted fields
    retain their current values (``exclude_unset=True``).

    Args:
        db: Active SQLAlchemy database session.
        appointment_id: Primary key of the appointment to update.
        data: Partial schema containing only the fields to change.

    Returns:
        The updated ``Appointment`` instance, or ``None`` if no record with
        the given ``appointment_id`` exists.
    """
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(appointment, field, value)
    db.commit()
    db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment_id: int) -> bool:
    """Delete an appointment from the database.

    Args:
        db: Active SQLAlchemy database session.
        appointment_id: Primary key of the appointment to delete.

    Returns:
        ``True`` if the record was found and deleted, ``False`` if no record
        with the given ``appointment_id`` exists.
    """
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        return False
    db.delete(appointment)
    db.commit()
    return True
