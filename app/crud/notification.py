from typing import Optional

from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate


def get_notification(db: Session, notification_id: int) -> Optional[Notification]:
    return db.query(Notification).filter(Notification.id == notification_id).first()


def get_notifications(db: Session, skip: int = 0, limit: int = 100) -> list[Notification]:
    return db.query(Notification).offset(skip).limit(limit).all()


def create_notification(db: Session, data: NotificationCreate) -> Notification:
    notification = Notification(**data.model_dump())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def mark_as_read(db: Session, notification_id: int) -> Optional[Notification]:
    notification = get_notification(db, notification_id)
    if not notification:
        return None
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


def delete_notification(db: Session, notification_id: int) -> bool:
    notification = get_notification(db, notification_id)
    if not notification:
        return False
    db.delete(notification)
    db.commit()
    return True
