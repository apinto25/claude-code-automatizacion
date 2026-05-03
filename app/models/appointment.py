from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
import enum

from app.database import Base


class AppointmentStatus(str, enum.Enum):
    """Valid lifecycle states for an appointment.

    Attributes:
        pending: Appointment has been created but not yet confirmed.
        confirmed: Appointment has been accepted by all parties.
        cancelled: Appointment was cancelled and will not take place.
    """

    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Appointment(Base):
    """SQLAlchemy ORM model representing a scheduled appointment.

    Attributes:
        id: Auto-incremented primary key.
        title: Short label for the appointment (max 255 chars).
        description: Optional longer description (max 1000 chars).
        scheduled_at: Date and time when the appointment is set to occur.
        location: Optional physical or virtual location (max 500 chars).
        status: Current lifecycle state; defaults to ``pending``.
        duration: Length of the appointment in minutes; must be a multiple
            of 15. Defaults to 30.
        created_at: UTC timestamp set automatically on record creation.
    """

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    scheduled_at = Column(DateTime, nullable=False)
    location = Column(String(500), nullable=True)
    status = Column(SAEnum(AppointmentStatus), default=AppointmentStatus.pending, nullable=False)
    duration = Column(Integer, default=30, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
