from fastapi import APIRouter, Request

from app.agents.postgres import PostgresAgent
from app.models.order import Order

order_router = APIRouter()

@order_router.get("/orders")
async def get_orders(request: Request, page: int = 1, per_page: int = 10):
    orders: list[Order] = await PostgresAgent().get_orders(page, per_page)
    
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

@order_router.get("/orders/{order_id}")
async def get_order_by_id(request: Request, order_id: int):
    order: Order = await PostgresAgent().get_order_by_id(order_id)
    
    if not order:
        return {
            "status": "error",
            "message": "Order not found"
        }
    
    return {
        "status": "success",
        "order": order
    }