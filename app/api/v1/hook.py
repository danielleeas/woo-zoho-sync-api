import json
from fastapi import APIRouter, Request
from app.services.sync import SyncService

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
        
        product_id = payload.get("id")
        webhook_id = payload.get("webhook_id")
        
        if product_id:
            product_type = payload.get("type")
            if product_type == "simple":
                print(f"Simple Product Created: ID: {product_id}")
                await SyncService().sync_create_product(payload)
            elif product_type == "variable":
                print(f"Variable Product Created: ID: {product_id}")
            else:
                print(f"Product Created: ID: {product_id}")
        else:
            print(f"Product Creation Webhook Received (Webhook ID: {webhook_id})")
        
        return {"message": "Webhook received successfully"}
    except Exception as e:
        # Log any other errors
        body = await request.body()
        print(f"Error processing webhook: {str(e)}. Raw body:", body)
        return {"error": "Error processing webhook"}, 400

@hook_router.post("/webhook/woocommerce/product/update")
async def webhook_woocommerce_product_update(request: Request):
    try:
        # First try to parse as JSON
        try:
            payload = await request.json()
        except json.JSONDecodeError:
            # If JSON parsing fails, try form data
            form_data = await request.form()
            payload = dict(form_data)
        
        print("Received WooCommerce Webhook:", json.dumps(payload, indent=2))
        
        product_id = payload.get("id")
        webhook_id = payload.get("webhook_id")
        
        if product_id:
            product_type = payload.get("type")
            if product_type == "simple":
                print(f"Simple Product Updated: ID: {product_id}")
                await SyncService().sync_update_product(payload)
            elif product_type == "variable":
                print(f"Variable Product Created: ID: {product_id}")
            else:
                print(f"Product Created: ID: {product_id}")
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
        webhook_id = payload.get("webhook_id")
        
        if product_id:
            await SyncService().sync_delete_product(product_id)
            print(f"Product Deleted: ID: {product_id}")
        else:
            print(f"Product Deletion Webhook Received (Webhook ID: {webhook_id})")
        
        return {"message": "Webhook received successfully"}
    except Exception as e:
        # Log any other errors
        body = await request.body()
        print(f"Error processing webhook: {str(e)}. Raw body:", body)
        return {"error": "Error processing webhook"}, 400

@hook_router.post("/webhook/woocommerce/product/restored")
async def webhook_woocommerce_product_restored(request: Request):
    try:
        # First try to parse as JSON
        try:
            payload = await request.json()
        except json.JSONDecodeError:
            # If JSON parsing fails, try form data
            form_data = await request.form()
            payload = dict(form_data)
        
        print("Received WooCommerce Webhook:", json.dumps(payload, indent=2))
        
        product_id = payload.get("id")
        webhook_id = payload.get("webhook_id")
        
        if product_id:
            product_type = payload.get("type")
            if product_type == "simple":
                print(f"Simple Product Restored: ID: {product_id}")
                await SyncService().sync_create_product(payload)
            elif product_type == "variable":
                print(f"Variable Product Restored: ID: {product_id}")
            else:
                print(f"Product Created: ID: {product_id}")
        else:
            print(f"Product Creation Webhook Received (Webhook ID: {webhook_id})")
        
        return {"message": "Webhook received successfully"}
    except Exception as e:
        # Log any other errors
        body = await request.body()
        print(f"Error processing webhook: {str(e)}. Raw body:", body)
        return {"error": "Error processing webhook"}, 400