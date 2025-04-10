from fastapi import APIRouter, Request

from app.agents.postgres import PostgresAgent
from app.api.deps import CurrentUser
from app.models.product import Product

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.get("/")
async def get_products(request: Request, current_user: CurrentUser, page: int = 1, per_page: int = 10):
    # Get all query parameters except page and per_page
    filters = dict(request.query_params)
    filters.pop('page', None)
    filters.pop('per_page', None)
    
    # Convert filter values based on Product model field types
    processed_filters = {}
    for key, value in filters.items():
        if hasattr(Product, key):
            field_type = Product.__annotations__.get(key)
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
    
    products: list[Product] = await PostgresAgent().get_products(page, per_page, filters=processed_filters)
    
    # Convert products to JSON-serializable format
    products_json = [product.model_dump() if hasattr(product, 'model_dump') else vars(product) for product in products]
    
    return {
        "status": "success",
        "data": {
            "products": products_json,
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total": len(products)
            }
        }
    }

@product_router.get("/{product_id}")
async def get_product_by_id(request: Request, product_id: int, current_user: CurrentUser):
    product: Product = await PostgresAgent().get_product(product_id)
    
    if not product:
        return {
            "status": "error",
            "message": "Product not found"
        }
    
    return {
        "status": "success",
        "product": product
    }

@product_router.get("/{product_id}/variations")
async def get_product_variations(request: Request, product_id: int, current_user: CurrentUser):
    variations: list[Product] = await PostgresAgent().get_product_variations(product_id)
    
    return {
        "status": "success",
        "variations": variations
    }

@product_router.get("/sku/{sku}")
async def get_products_by_sku(request: Request, sku: str, current_user: CurrentUser):
    product: Product = await PostgresAgent().search_products_by_sku(sku)
    
    return {
        "status": "success",
        "product": product
    }