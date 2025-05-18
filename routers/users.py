from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud
from ..database import get_db
from ..ml import user_recommendation

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/{user_id}/recommendations")
def get_recommendations(user_id: int, db: Session = Depends(get_db), top_n: int = 5):
    # Check user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get all bookings grouped by user_id
    bookings = db.query(crud.models.Booking).all()
    user_bookings = {}
    for b in bookings:
        user_bookings.setdefault(b.user_id, []).append(b.event_id)
    
    # Get all events
    events = db.query(crud.models.Event).all()
    events_data = [{"id": e.id, "name": e.name, "category": e.category} for e in events]
    
    # Get recommendations
    recommended_events = user_recommendation.recommend_events(user_id, user_bookings, events_data, top_n=top_n)
    
    return {"user_id": user_id, "recommendations": recommended_events}
