import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.services.wcmc.product import ProductService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the task but don't await it
    product_task = asyncio.create_task(ProductService().check_duplicated_name_variable_products())
    
    # Store the task in app state and continue immediately
    app.state.product_task = product_task
    
    # Add error handling for the background task
    async def monitor_task():
        try:
            result = await product_task
            print("Product fetch completed:", result)
        except Exception as e:
            print(f"Product fetch failed: {e}")
    
    # Start the monitoring task without waiting
    asyncio.create_task(monitor_task())
    
    yield
    
    # Cleanup
    if not product_task.done():
        product_task.cancel()
        try:
            await product_task
        except asyncio.CancelledError:
            pass

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

