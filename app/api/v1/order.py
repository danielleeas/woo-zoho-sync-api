from fastapi import APIRouter, Request
from app.agents.postgres import PostgresAgent
from app.agents.wcmc import WCMC
from app.models.order import Order
from app.api.deps import CurrentUser

order_router = APIRouter()

@order_router.get("/orders")
async def get_orders(request: Request, current_user: CurrentUser, page: int = 1, per_page: int = 10):
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
async def get_order_by_id(request: Request, order_id: int, current_user: CurrentUser):
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

@order_router.post("/orders/{order_id}/status")
async def update_order_status(request: Request, order_id: int, status: str, current_user: CurrentUser):
    order: Order = await PostgresAgent().update_order_status(order_id, status)
    
    if not order:
        return {
            "status": "error",
            "message": "Order not found"
        }
    
    await WCMC().update_order_status(order_id, status)
    
    return {
        "status": "success",
        "order": order
    }

@order_router.get("/orders/{order_id}/track")
async def track_order(request: Request, order_id: int, current_user: CurrentUser):
    order: Order = await PostgresAgent().get_order_by_id(order_id)
    
    if not order:
        return {
            "status": "error",
            "message": "Order not found"
        }
    
    notes = WCMC().track_order(order_id)
    
    if not notes:
        return {
            "status": "error",
            "message": "No notes found"
        }
    
    all_notes = []
    
    for note in notes:
        single_note = {
            "note": note["note"],
            "date": note["date_created"]
        }
        all_notes.append(single_note)
    
    return {
        "status": "success",
        "notes": all_notes
    }