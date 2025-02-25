from woocommerce import API
from app.config import settings
import asyncio

class WCMC:
    def __init__(self):
        self.wcapi = API(
            url=settings.WCM_URL,
            consumer_key=settings.WCM_CONSUMER_KEY,
            consumer_secret=settings.WCM_CONSUMER_SECRET,
            wp_api=True,
            version="wc/v3",
            timeout=30,
            verify=False
        )
    
    async def get_products(self, page: int = 1, per_page: int = 100, params: dict = {}):
        try:
            # Use asyncio.to_thread if the API call is blocking
            products = await asyncio.to_thread(
                self.wcapi.get,
                "products",
                params={"page": page, "per_page": per_page, **params}
            )
            return products.json()
        except Exception as e:
            raise Exception(f"Error fetching products: {str(e)}")
    
    async def get_product(self, product_id: int):
        product = await self.wcapi.get(f"products/{product_id}")
        return product
    
    async def delete_product(self, product_id: int):
        try:
            # Use asyncio.to_thread if the API call is blocking
            product = await asyncio.to_thread(
                self.wcapi.delete,
                f"products/{product_id}",
                params={"force": True}
            )
            return product.json()
        except Exception as e:
            raise Exception(f"Error deleting product: {str(e)}")
    
    async def get_product_variations(self, product_id: int):
        try:
            # Use asyncio.to_thread if the API call is blocking
            products = await asyncio.to_thread(
                self.wcapi.get,
                f"products/{product_id}/variations",
            )
            return products.json()
        except Exception as e:
            raise Exception(f"Error fetching products: {str(e)}")
    
    async def get_categories(self, per_page: int = 100, page: int = 1):
        try:
            # Use asyncio.to_thread if the API call is blocking
            response = await asyncio.to_thread(
                self.wcapi.get,
                "products/categories",
                params={
                    "per_page": per_page,
                    "page": page
                }
            )
            return response.json()
        except Exception as e:
            raise Exception(f"Error fetching categories: {str(e)}")
    
    async def get_orders(self, per_page: int = 100, page: int = 1):
        try:
            # Use asyncio.to_thread if the API call is blocking
            response = await asyncio.to_thread(
                self.wcapi.get,
                "orders",
                params={
                    "per_page": per_page,
                    "page": page,
                    "status": "completed"
                }
            )
            return response.json()
        except Exception as e:
            raise Exception(f"Error fetching orders: {str(e)}")
    
    async def get_customers(self, per_page: int = 100, page: int = 1):
        try:
            response = await asyncio.to_thread(
                self.wcapi.get,
                "customers",
                params={"per_page": per_page, "page": page}
            )
            return response.json()
        except Exception as e:
            raise Exception(f"Error fetching customers: {str(e)}")