import os, json
import unicodedata
from bs4 import BeautifulSoup

from app.agents.postgres import PostgresAgent
from app.models.line_items import LineItemsBase
from app.models.order import OrderBase
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
            purchase_price=str(product_data["purchase_price"] if product_data["purchase_price"] else ""),
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
    
    async def sync_create_order(self, order_data: dict):
        try:
            order_base = OrderBase(
                order_id=order_data["id"],
                customer_id=order_data["customer_id"],
                status=order_data["status"],
                currency=order_data["currency"],
                total=order_data["total"],
                order_key=order_data["order_key"],
                prices_include_tax=order_data["prices_include_tax"],
                discount_total=order_data["discount_total"],
                discount_tax=order_data["discount_tax"],
                shipping_total=order_data["shipping_total"],
                shipping_tax=order_data["shipping_tax"],
                cart_tax=order_data["cart_tax"],
                total_tax=order_data["total_tax"],
                billing_first_name=order_data["billing"]["first_name"],
                billing_last_name=order_data["billing"]["last_name"],
                billing_company=order_data["billing"]["company"],
                billing_address_1=order_data["billing"]["address_1"],
                billing_address_2=order_data["billing"]["address_2"],
                billing_city=order_data["billing"]["city"],
                billing_state=order_data["billing"]["state"],
                billing_postcode=order_data["billing"]["postcode"],
                billing_country=order_data["billing"]["country"],
                billing_email=order_data["billing"]["email"],
                billing_phone=order_data["billing"]["phone"],
                shipping_first_name=order_data["shipping"]["first_name"],
                shipping_last_name=order_data["shipping"]["last_name"],
                shipping_company=order_data["shipping"]["company"],
                shipping_address_1=order_data["shipping"]["address_1"],
                shipping_address_2=order_data["shipping"]["address_2"],
                shipping_city=order_data["shipping"]["city"],
                shipping_state=order_data["shipping"]["state"],
                shipping_postcode=order_data["shipping"]["postcode"],
                shipping_country=order_data["shipping"]["country"],
                payment_method=order_data["payment_method"],
                payment_method_title=order_data["payment_method_title"],
                transaction_id=order_data["transaction_id"],
                customer_ip_address=order_data["customer_ip_address"],
                customer_user_agent=order_data["customer_user_agent"],
                created_via=order_data["created_via"],
                customer_note=order_data["customer_note"],
                date_completed=order_data["date_completed"],
                date_created=order_data["date_created"],
                date_modified=order_data["date_modified"],
                date_paid=order_data["date_paid"],
                cart_hash=order_data["cart_hash"],
                number=order_data["number"],
                payment_url=order_data["payment_url"],
                currency_symbol=order_data["currency_symbol"],
            )
            db_order = await self.postgres.insert_order(order_base)
            if not db_order:
                return False, order_base
            
            for item in order_data["line_items"]:
                line_item = LineItemsBase(
                    order_id=db_order.order_id,
                    name=item["name"],
                    product_id=item["product_id"],
                    variation_id=item["variation_id"],
                    quantity=item["quantity"],
                    tax_class=item["tax_class"],
                    subtotal=item["subtotal"],
                    subtotal_tax=item["subtotal_tax"],
                    total=item["total"],
                    total_tax=item["total_tax"],
                    sku=item["sku"],
                    price=int(float(item["price"])) if item["price"] else 0
                )
                await self.postgres.insert_order_line(line_item)
                
            return True, db_order
        except Exception as e:
            print(f"Error inserting order: {e}")
            return False
    
    async def sync_update_order(self, order_data: dict):
        try:
            order_base = OrderBase(
                order_id=order_data["id"],
                customer_id=order_data["customer_id"],
                status=order_data["status"],
                currency=order_data["currency"],
                total=order_data["total"],
                order_key=order_data["order_key"],
                prices_include_tax=order_data["prices_include_tax"],
                discount_total=order_data["discount_total"],
                discount_tax=order_data["discount_tax"],
                shipping_total=order_data["shipping_total"],
                shipping_tax=order_data["shipping_tax"],
                cart_tax=order_data["cart_tax"],
                total_tax=order_data["total_tax"],
                billing_first_name=order_data["billing"]["first_name"],
                billing_last_name=order_data["billing"]["last_name"],
                billing_company=order_data["billing"]["company"],
                billing_address_1=order_data["billing"]["address_1"],
                billing_address_2=order_data["billing"]["address_2"],
                billing_city=order_data["billing"]["city"],
                billing_state=order_data["billing"]["state"],
                billing_postcode=order_data["billing"]["postcode"],
                billing_country=order_data["billing"]["country"],
                billing_email=order_data["billing"]["email"],
                billing_phone=order_data["billing"]["phone"],
                shipping_first_name=order_data["shipping"]["first_name"],
                shipping_last_name=order_data["shipping"]["last_name"],
                shipping_company=order_data["shipping"]["company"],
                shipping_address_1=order_data["shipping"]["address_1"],
                shipping_address_2=order_data["shipping"]["address_2"],
                shipping_city=order_data["shipping"]["city"],
                shipping_state=order_data["shipping"]["state"],
                shipping_postcode=order_data["shipping"]["postcode"],
                shipping_country=order_data["shipping"]["country"],
                payment_method=order_data["payment_method"],
                payment_method_title=order_data["payment_method_title"],
                transaction_id=order_data["transaction_id"],
                customer_ip_address=order_data["customer_ip_address"],
                customer_user_agent=order_data["customer_user_agent"],
                created_via=order_data["created_via"],
                customer_note=order_data["customer_note"],
                date_completed=order_data["date_completed"],
                date_created=order_data["date_created"],
                date_modified=order_data["date_modified"],
                date_paid=order_data["date_paid"],
                cart_hash=order_data["cart_hash"],
                number=order_data["number"],
                payment_url=order_data["payment_url"],
                currency_symbol=order_data["currency_symbol"],
            )
            
            db_order = await self.postgres.update_order(order_data["id"], order_base)
            if not db_order:
                return False, order_base
            
            await self.postgres.delete_order_line(order_data["id"])
            
            for item in order_data["line_items"]:
                line_item = LineItemsBase(
                    order_id=db_order.order_id,
                    name=item["name"],
                    product_id=item["product_id"],
                    variation_id=item["variation_id"],
                    quantity=item["quantity"],
                    tax_class=item["tax_class"],
                    subtotal=item["subtotal"],
                    subtotal_tax=item["subtotal_tax"],
                    total=item["total"],
                    total_tax=item["total_tax"],
                    sku=item["sku"],
                    price=int(float(item["price"])) if item["price"] else 0
                )
                await self.postgres.insert_order_line(line_item)
        except Exception as e:
            print(f"Error inserting order: {e}")
            return False
    
    async def sync_delete_order(self, order_id: int):
        try:
            await self.postgres.delete_order(order_id)
            return True
        except Exception as e:
            print(f"Error deleting order: {e}")
            return False
    

