import json
from fastapi import APIRouter, Request

hook_router = APIRouter()

@hook_router.post("/webhook/woocommerce/product/create")
async def webhook_woocommerce_product_create(request: Request):
    try:
        # First try to parse as JSON
        try:
            payload = await request.json()
        except json.JSONDecodeError:
            # If JSON parsing fails, try form data
            form_data = await request.form()
            payload = dict(form_data)
        
        print("Received WooCommerce Webhook:", json.dumps(payload, indent=2))
        
        # Process the product data (e.g., store in database, send notification)
        product_id = payload.get("id")
        product_name = payload.get("name")
        webhook_id = payload.get("webhook_id")
        
        if product_id and product_name:
            print(f"Product Created: {product_name} (ID: {product_id})")
        else:
            print(f"Product Creation Webhook Received (Webhook ID: {webhook_id})")
        
        return {"message": "Webhook received successfully"}
    except Exception as e:
        # Log any other errors
        body = await request.body()
        print(f"Error processing webhook: {str(e)}. Raw body:", body)
        return {"error": "Error processing webhook"}, 400

@hook_router.post("/webhook/woocommerce/product/delete")
async def webhook_woocommerce_product_delete(request: Request):
    try:
        # First try to parse as JSON
        try:
            payload = await request.json()
        except json.JSONDecodeError:
            # If JSON parsing fails, try form data
            form_data = await request.form()
            payload = dict(form_data)
        
        print("Received WooCommerce Webhook:", json.dumps(payload, indent=2))
        
        # Process the product data (e.g., store in database, send notification)
        product_id = payload.get("id")
        product_name = payload.get("name")
        webhook_id = payload.get("webhook_id")
        
        if product_id and product_name:
            print(f"Product Deleted: {product_name} (ID: {product_id})")
        else:
            print(f"Product Deletion Webhook Received (Webhook ID: {webhook_id})")
        
        return {"message": "Webhook received successfully"}
    except Exception as e:
        # Log any other errors
        body = await request.body()
        print(f"Error processing webhook: {str(e)}. Raw body:", body)
        return {"error": "Error processing webhook"}, 400