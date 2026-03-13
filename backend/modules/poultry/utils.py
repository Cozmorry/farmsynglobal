# backend/modules/poultry/utils.py

from datetime import date
from sqlalchemy.orm import Session
from backend.modules.poultry import models, schemas

# Daily activity types (without store usage or health)
DAILY_ACTIVITY_TYPES = [
    "Feeding",
    "Watering",
    "Cleaning",
    "Egg Collection",
    "Observation / Behavior Check",
    "Lighting Adjustment",
    "Record Mortality",
]

def create_daily_activities(db: Session, batch_id: int, performed_by: str = None):
    today = date.today()

    # Check if today's activities already exist
    existing = db.query(models.PoultryActivity).filter(
        models.PoultryActivity.poultry_batch_id == batch_id,
        models.PoultryActivity.date == today
    ).all()

    if existing:
        return existing  # Avoid duplicates

    created_activities = []
    for activity_type in DAILY_ACTIVITY_TYPES:
        activity_data = schemas.PoultryActivityCreate(
            poultry_batch_id=batch_id,
            date=today,
            activity_type=activity_type,
            performed_by=performed_by,
            cost=0.0,
            feed_used_kg=0.0 if activity_type == "Feeding" else None,
            water_used_l=0.0 if activity_type == "Watering" else None,
            mortality=0 if activity_type == "Record Mortality" else None,
        )
        activity = models.PoultryActivity(**activity_data.dict())
        db.add(activity)
        created_activities.append(activity)

    db.commit()

    for activity in created_activities:
        db.refresh(activity)

    return created_activities
