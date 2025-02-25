from fastapi import APIRouter, Request

from app.agents.postgres import PostgresAgent
from app.models.product import Product

product_router = APIRouter()

@product_router.get("/products")
async def get_products(request: Request, page: int = 1, per_page: int = 10):
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

@product_router.get("/products/search")
async def search_products(name: str, page: int = 1, per_page: int = 10):
    products: list[Product] = await PostgresAgent().search_products_by_name(name, page, per_page)
    
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
