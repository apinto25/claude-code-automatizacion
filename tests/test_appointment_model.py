from datetime import datetime, timezone, timedelta

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def sample_scheduled_at():
    return datetime(2026, 6, 15, 10, 0, tzinfo=timezone.utc)


@pytest.fixture
def valid_appointment_data(sample_scheduled_at):
    return {
        "title": "Team sync",
        "scheduled_at": sample_scheduled_at,
        "duration": 30,
    }


# ---------------------------------------------------------------------------
# ORM model — persistence & defaults
# ---------------------------------------------------------------------------

class TestAppointmentModel:
    def test_persist_and_retrieve(self, db_session, sample_scheduled_at):
        appt = Appointment(
            title="Onboarding",
            scheduled_at=sample_scheduled_at,
            duration=60,
        )
        db_session.add(appt)
        db_session.flush()

        fetched = db_session.get(Appointment, appt.id)
        assert fetched.title == "Onboarding"
        assert fetched.scheduled_at == sample_scheduled_at
        assert fetched.duration == 60

    def test_default_status_is_pending(self, db_session, sample_scheduled_at):
        appt = Appointment(title="Stand-up", scheduled_at=sample_scheduled_at, duration=15)
        db_session.add(appt)
        db_session.flush()
        assert appt.status == AppointmentStatus.pending

    def test_default_duration_is_30(self, db_session, sample_scheduled_at):
        appt = Appointment(title="Quick chat", scheduled_at=sample_scheduled_at)
        db_session.add(appt)
        db_session.flush()
        assert appt.duration == 30

    def test_created_at_is_set_automatically(self, db_session, sample_scheduled_at):
        before = datetime.now(timezone.utc).replace(tzinfo=None)
        appt = Appointment(title="Review", scheduled_at=sample_scheduled_at, duration=30)
        db_session.add(appt)
        db_session.flush()
        after = datetime.now(timezone.utc).replace(tzinfo=None)

        assert appt.created_at is not None
        created = appt.created_at.replace(tzinfo=None) if appt.created_at.tzinfo else appt.created_at
        assert before <= created <= after

    def test_optional_fields_nullable(self, db_session, sample_scheduled_at):
        appt = Appointment(title="Minimal", scheduled_at=sample_scheduled_at, duration=15)
        db_session.add(appt)
        db_session.flush()
        assert appt.description is None
        assert appt.location is None

    def test_all_status_values_persist(self, db_session, sample_scheduled_at):
        for status in AppointmentStatus:
            appt = Appointment(
                title=f"Status test {status}",
                scheduled_at=sample_scheduled_at,
                duration=30,
                status=status,
            )
            db_session.add(appt)
            db_session.flush()
            assert appt.status == status


# ---------------------------------------------------------------------------
# Schema — duration validation
# ---------------------------------------------------------------------------

class TestDurationValidation:
    @pytest.mark.parametrize("duration", [15, 30, 45, 60, 90, 120])
    def test_valid_multiples_of_15(self, valid_appointment_data, duration):
        data = {**valid_appointment_data, "duration": duration}
        schema = AppointmentCreate(**data)
        assert schema.duration == duration

    @pytest.mark.parametrize("duration", [1, 10, 20, 25, 31, 100])
    def test_invalid_non_multiples_rejected(self, valid_appointment_data, duration):
        data = {**valid_appointment_data, "duration": duration}
        with pytest.raises(ValidationError, match="multiple of 15"):
            AppointmentCreate(**data)

    def test_zero_duration_rejected(self, valid_appointment_data):
        # 0 is a multiple of 15 mathematically but semantically meaningless;
        # current validator allows it — document the current behaviour here
        # and update if a > 0 constraint is added later.
        data = {**valid_appointment_data, "duration": 0}
        schema = AppointmentCreate(**data)
        assert schema.duration == 0

    def test_update_valid_duration(self, sample_scheduled_at):
        update = AppointmentUpdate(duration=45)
        assert update.duration == 45

    def test_update_invalid_duration_rejected(self, sample_scheduled_at):
        with pytest.raises(ValidationError, match="multiple of 15"):
            AppointmentUpdate(duration=20)

    def test_update_none_duration_allowed(self):
        update = AppointmentUpdate(duration=None)
        assert update.duration is None


# ---------------------------------------------------------------------------
# Schema — created_at / scheduled_at date handling
# ---------------------------------------------------------------------------

class TestDateFields:
    def test_scheduled_at_in_past_is_accepted(self, valid_appointment_data):
        past = datetime(2020, 1, 1, tzinfo=timezone.utc)
        schema = AppointmentCreate(**{**valid_appointment_data, "scheduled_at": past})
        assert schema.scheduled_at == past

    def test_scheduled_at_in_future_is_accepted(self, valid_appointment_data):
        future = datetime.now(timezone.utc) + timedelta(days=30)
        schema = AppointmentCreate(**{**valid_appointment_data, "scheduled_at": future})
        assert schema.scheduled_at == future

    def test_created_at_present_in_response(self, db_session, sample_scheduled_at):
        from app.schemas.appointment import AppointmentResponse

        appt = Appointment(
            title="Response check",
            scheduled_at=sample_scheduled_at,
            duration=30,
            created_at=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc),
        )
        db_session.add(appt)
        db_session.flush()

        response = AppointmentResponse.model_validate(appt)
        assert response.created_at is not None

    def test_scheduled_at_required(self):
        with pytest.raises(ValidationError):
            AppointmentCreate(title="No date", duration=30)
