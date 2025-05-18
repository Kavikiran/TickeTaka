from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud
from ..database import get_db
from ..ml import demand_forecasting, dynamic_pricing

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

# Existing endpoints...

@router.get("/{event_id}/price")
def get_dynamic_price(event_id: int, days: int = 30, db: Session = Depends(get_db)):
    event = crud.get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    max_capacity = event.capacity
    base_price = event.base_price  # Make sure your Event model has this field
    
    # Get forecasted sales
    sales_data = demand_forecasting.simulate_ticket_sales(event_id=event_id)
    model = demand_forecasting.train_forecast_model(sales_data)
    forecast_df = demand_forecasting.forecast_sales(model, periods=days)
    
    # Use the predicted sales for the first forecast day (or average)
    predicted_sales = int(forecast_df.iloc[0]['yhat'])
    
    price = dynamic_pricing.calculate_dynamic_price(base_price, predicted_sales, max_capacity)
    
    return {
        "event_id": event_id,
        "base_price": base_price,
        "predicted_sales": predicted_sales,
        "max_capacity": max_capacity,
        "dynamic_price": price
    }
