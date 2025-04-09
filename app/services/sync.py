import os, json
import unicodedata
from bs4 import BeautifulSoup

from app.agents.postgres import PostgresAgent
from app.models.product import ProductBase

class SyncService:
    def __init__(self):
        self.postgres = PostgresAgent()
        
    async def sync_create_product(self, product_data: dict):
        categories = [category["slug"] for category in product_data["categories"]]
        images = []
        if product_data["images"]:
            for image in product_data["images"]:
                images.append(image["src"])
    
        attribute_name = ""
        attribute_value = ""
        if len(product_data["attributes"]) > 0:
            attribute_name = product_data["attributes"][0]["name"]
            if product_data["type"] == "variation":
                attribute_value = product_data["attributes"][0]["option"]
        
        final_description = ""
        if product_data["description"]:
            text = product_data["description"]
            soup = BeautifulSoup(text, 'html.parser')
            # Clean text of emojis and invalid characters
            plain_text = soup.get_text(separator=' ').strip()
            # Remove non-BMP characters, convert special characters to ASCII, and remove < >
            cleaned_text = unicodedata.normalize('NFKD', plain_text).encode('ascii', 'ignore').decode('ascii')
            cleaned_text = cleaned_text.replace('<', '').replace('>', '')
            truncated_description = cleaned_text[:2000]
            final_description = truncated_description
        else:
            final_description = "No Description"
            
        product_data['description'] = final_description if final_description != "" else "No Description"
        
        product_base = ProductBase(
            parent_id=product_data["parent_id"],
            product_id=product_data["id"],
            name=product_data["name"],
            slug=product_data["slug"],
            permalink=product_data["permalink"],
            date_created=product_data["date_created"],
            date_modified=product_data["date_modified"],
            type=product_data["type"],
            status=product_data["status"],
            featured=product_data["featured"],
            description=product_data["description"],
            sku=product_data["sku"],
            price=str(product_data["price"]),
            regular_price=str(product_data["regular_price"]),
            stock_quantity=product_data["stock_quantity"] if product_data["stock_quantity"] and product_data["stock_quantity"] >= 0 else 0,
            weight=product_data["weight"],
            length=product_data["dimensions"]["length"],
            width=product_data["dimensions"]["width"],
            height=product_data["dimensions"]["height"],
            categories=categories,
            images=images,
            attribute_name=attribute_name,
            attribute_value=attribute_value,
        )
        
        try:
            db_product = await self.postgres.insert_product(product_base)
            return db_product
        except Exception as e:
            print(f"Error inserting product: {e}")
            return False

    async def sync_delete_product(self, product_id: int):
        try:
            await self.postgres.delete_product(product_id)
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    async def sync_update_product(self, product_data: dict):
        categories = [category["slug"] for category in product_data["categories"]]
        images = []
        if product_data["images"]:
            for image in product_data["images"]:
                images.append(image["src"])
    
        attribute_name = ""
        attribute_value = ""
        if len(product_data["attributes"]) > 0:
            attribute_name = product_data["attributes"][0]["name"]
            if product_data["type"] == "variation":
                attribute_value = product_data["attributes"][0]["option"]
        
        final_description = ""
        if product_data["description"]:
            text = product_data["description"]
            soup = BeautifulSoup(text, 'html.parser')
            # Clean text of emojis and invalid characters
            plain_text = soup.get_text(separator=' ').strip()
            # Remove non-BMP characters, convert special characters to ASCII, and remove < >
            cleaned_text = unicodedata.normalize('NFKD', plain_text).encode('ascii', 'ignore').decode('ascii')
            cleaned_text = cleaned_text.replace('<', '').replace('>', '')
            truncated_description = cleaned_text[:2000]
            final_description = truncated_description
        else:
            final_description = "No Description"
            
        product_data['description'] = final_description if final_description != "" else "No Description"
        
        product_base = ProductBase(
            parent_id=product_data["parent_id"],
            product_id=product_data["id"],
            name=product_data["name"],
            slug=product_data["slug"],
            permalink=product_data["permalink"],
            date_created=product_data["date_created"],
            date_modified=product_data["date_modified"],
            type=product_data["type"],
            status=product_data["status"],
            featured=product_data["featured"],
            description=product_data["description"],
            sku=product_data["sku"],
            price=str(product_data["price"]),
            regular_price=str(product_data["regular_price"]),
            purchase_price=str(product_data["purchase_price"]),
            stock_quantity=product_data["stock_quantity"] if product_data["stock_quantity"] and product_data["stock_quantity"] >= 0 else 0,
            weight=product_data["weight"],
            length=product_data["dimensions"]["length"],
            width=product_data["dimensions"]["width"],
            height=product_data["dimensions"]["height"],
            categories=categories,
            images=images,
            attribute_name=attribute_name,
            attribute_value=attribute_value,
        )
        
        try:
            db_product = await self.postgres.update_product(product_data["id"], product_base)
            return db_product
        except Exception as e:
            print(f"Error inserting product: {e}")
            return False

