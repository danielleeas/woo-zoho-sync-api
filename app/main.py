import asyncio
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

# from app.services.crud import CRUDService
# from app.services.wcmc.product import ProductService
# from app.services.wcmc.category import CategoryService
from app.api.v1.oauth import zoho_router
from app.api.v1.product import product_router
from app.api.v1.order import order_router
from app.api.v1.hook import hook_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Create the task but don't await it
#     category_task = asyncio.create_task(CRUDService().create_customers())
    
#     # Store the task in app state and continue immediately
#     app.state.category_task = category_task
    
#     # Add error handling for the background task
#     async def monitor_task():
#         try:
#             result = await category_task
#             print("Category fetch completed:", result)
#         except Exception as e:
#             print(f"Category fetch failed: {e}")
    
#     # Start the monitoring task without waiting
#     asyncio.create_task(monitor_task())
    
#     yield
    
#     # Cleanup
#     if not category_task.done():
#         category_task.cancel()
#         try:
#             await category_task
#         except asyncio.CancelledError:
#             pass

app = FastAPI()
# app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World Lee"}

app.include_router(zoho_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(hook_router, prefix="/api/v1")