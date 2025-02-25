from fastapi import APIRouter, Request

from app.agents.postgres import PostgresAgent
from app.models.order import Order

order_router = APIRouter()

@order_router.get("/orders")
async def get_orders(request: Request, page: int = 1, per_page: int = 10):
    # Get all query parameters except page and per_page
    filters = dict(request.query_params)
    filters.pop('page', None)
    filters.pop('per_page', None)
    
    # Convert filter values based on Product model field types
    processed_filters = {}
    for key, value in filters.items():
        if hasattr(Order, key):
            field_type = Order.__annotations__.get(key)
            if field_type == int:
                try:
                    # Handle both single values and lists of values
                    if isinstance(value, list):
                        processed_filters[key] = [int(v) for v in value]
                    else:
                        processed_filters[key] = int(value)
                except ValueError:
                    continue
            elif field_type == bool:
                processed_filters[key] = value.lower() in ('true', '1', 'yes')
            else:
                processed_filters[key] = value
    
    orders: list[Order] = await PostgresAgent().get_orders(page, per_page, filters=processed_filters)
    
    return {
        "status": "success",
        "data": {
            "orders": orders,
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total": len(orders)
            }
        }
    }