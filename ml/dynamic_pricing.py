# backend/ml/dynamic_pricing.py

def calculate_dynamic_price(base_price: float, predicted_sales: int, max_capacity: int) -> float:
    """
    Adjust price based on predicted sales.
    - If predicted sales are near max capacity, increase price by up to 50%.
    - If predicted sales are low (<30%), decrease price by up to 20%.
    """
    if max_capacity <= 0:
        return base_price  # Avoid division by zero
    
    demand_ratio = predicted_sales / max_capacity
    
    if demand_ratio >= 1:
        price = base_price * 1.5  # max 50% increase
    elif demand_ratio >= 0.7:
        price = base_price * (1 + 0.5 * (demand_ratio - 0.7) / 0.3)
    elif demand_ratio < 0.3:
        price = base_price * (1 - 0.2 * (0.3 - demand_ratio) / 0.3)
    else:
        price = base_price
    
    return round(price, 2)
