from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/", response_model=list[schemas.AppointmentResponse])
def list_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Return a paginated list of appointments.

    Args:
        skip: Number of records to skip for pagination. Defaults to 0.
        limit: Maximum number of records to return. Defaults to 100.
        db: Database session injected by FastAPI.

    Returns:
        A list of ``AppointmentResponse`` objects, possibly empty.
    """
    return crud.get_appointments(db, skip=skip, limit=limit)


@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Retrieve a single appointment by ID.

    Args:
        appointment_id: Primary key of the appointment to fetch.
        db: Database session injected by FastAPI.

    Returns:
        The ``AppointmentResponse`` for the requested appointment.

    Raises:
        HTTPException: 404 if no appointment with the given ID exists.
    """
    appointment = crud.get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment


@router.post("/", response_model=schemas.AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(data: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    """Create a new appointment.

    Args:
        data: Request body with the appointment fields. ``duration`` must be
            a positive multiple of 15 minutes.
        db: Database session injected by FastAPI.

    Returns:
        The newly created ``AppointmentResponse``, including the generated
        ``id`` and ``created_at`` timestamp.
    """
    return crud.create_appointment(db, data)


@router.patch("/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(
    appointment_id: int, data: schemas.AppointmentUpdate, db: Session = Depends(get_db)
):
    """Partially update an existing appointment.

    Only the fields present in the request body are modified; all other
    fields retain their current values.

    Args:
        appointment_id: Primary key of the appointment to update.
        data: Request body containing one or more fields to change.
            ``duration``, if provided, must be a multiple of 15 minutes.
        db: Database session injected by FastAPI.

    Returns:
        The updated ``AppointmentResponse``.

    Raises:
        HTTPException: 404 if no appointment with the given ID exists.
    """
    appointment = crud.update_appointment(db, appointment_id, data)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Delete an appointment.

    Args:
        appointment_id: Primary key of the appointment to delete.
        db: Database session injected by FastAPI.

    Returns:
        No content (HTTP 204) on success.

    Raises:
        HTTPException: 404 if no appointment with the given ID exists.
    """
    deleted = crud.delete_appointment(db, appointment_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
