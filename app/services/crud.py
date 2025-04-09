import os, json
import unicodedata
from bs4 import BeautifulSoup

from app.agents.wcmc import WCMC
from app.agents.postgres import PostgresAgent
from app.models.category import CategoryBase
from app.models.product import ProductBase
from app.models.customer import CustomerBase
from app.models.order import OrderBase
from app.models.line_items import LineItemsBase

class CRUDService:
    def __init__(self):
        self.postgres = PostgresAgent()
        self.wcmc = WCMC()
        
    async def _save_category(self, category_data):
        """Helper method to create and save a category"""
        category_base = CategoryBase(
            name=category_data["name"],
            slug=category_data["url"],
        )
        
        try:
            await self.postgres.insert_category(category_base)
            return True
        except Exception as e:
            print(f"Error inserting category: {e}")
            return False

    async def create_categories(self):
        """Create categories from JSON files"""
        self.current_depth = 0
        total_count = success_count = failed_count = 0
        failed_categories = []

        while True:
            filename = f"data/wcmc/categories_level_{self.current_depth}.json"
            if not os.path.exists(filename):
                break

            with open(filename, 'r') as f:
                categories = json.load(f)

            for category in categories:
                print(category)
                result = await self._save_category(category)
                if result:
                    success_count += 1
                else:
                    failed_categories.append(category)
                    failed_count += 1
                total_count += 1

            print(f"Depth {self.current_depth} - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
            self.current_depth += 1

        print(f"Final totals - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
        return "Categories created"
    
    async def calc_total_categories(self):
        count = 0
        total_count = 0
        while True:
            filename = f"data/wcmc/categories_level_{count}.json"
            if not os.path.exists(filename):
                break
            with open(filename, 'r') as f:
                categories = json.load(f)
                total_count += len(categories)
            count += 1
        
        print(f"Total categories: {total_count}")
        return total_count
    
    async def _save_product(self, product_data):
        """Helper method to create and save a product"""
        
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
            db_product = await self.postgres.insert_product(product_base)
            return db_product
        except Exception as e:
            print(f"Error inserting product: {e}")
            return False
    
    async def create_products(self):
        count = 1
        total_count = success_count = failed_count = 0
        failed_products = []
        while True:
            filename = f"data/wcmc/final/products_{count}.json"
            if not os.path.exists(filename):
                break
            
            with open(filename, 'r') as f:
                products = json.load(f)
            
            for product in products:
                print("adding product: ", product["name"], " - count: ", total_count)
                result = await self._save_product(product)
                if result:
                    success_count += 1
                else:
                    failed_products.append(product)
                    failed_count += 1
                total_count += 1
            
            print(f"Products level {count} - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
            count += 1
        
        print(f"Final totals - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
        return total_count
    
    async def all_variable_products(self):
        try:
            products = []
            page = 1
            per_page = 100
            current_file_number = 1
            products_per_file = 100
            params = {
                "status": "publish",
                "type": "variable"
            }
            while True:
                try:
                    page_products = await self.wcmc.get_products(page, per_page, params)
                    if not page_products:  # If we get an empty response, we've reached the end
                        break
                    products.extend(page_products)
                    while len(products) >= products_per_file:
                        filename = f"data/wcmc/variable/products_{current_file_number}.json"
                        batch = products[:products_per_file]
                        products = products[products_per_file:]
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(batch, f, indent=4, ensure_ascii=False)
                        
                        print(f"Saved {filename}")
                        current_file_number += 1
                    page += 1
                except Exception as e:
                    print(f"Error on page {page}: {str(e)}")
                    return {"error": str(e), "last_successful_page": page - 1}
            
            if products:  # Save any remaining products
                filename = f"data/wcmc/variable/products_{current_file_number}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(products, f, indent=4, ensure_ascii=False)
                print(f"Saved {filename}")
                
            return {
                "success": True,
                "message": f"Products saved to data/wcmc/variable/products_1.json through data/wcmc/variable/products_{current_file_number}.json"
            }
            
        except Exception as e:
            return {"error": f"Fatal error: {str(e)}"}
    
    async def get_product_variations(self):
        count = 1
        while True:
            if not os.path.exists(f"data/wcmc/variable/products_{count}.json"):
                break
            
            with open(f"data/wcmc/variable/products_{count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                if product['type'] == 'variable':
                    print(product['name'])
                    variations = await self.wcmc.get_product_variations(product['id'])
                    filename = f"data/wcmc/variations/variations_{product['id']}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(variations, f, indent=4, ensure_ascii=False)
                    print(f"Saved {filename}")
            count += 1
            
        return f"Product Variations saved"
    
    async def create_variations_products(self):
        count = 1
        total_count = success_count = failed_count = 0
        failed_products = []
        while True:
            if not os.path.exists(f"data/wcmc/variable/products_{count}.json"):
                break
            
            with open(f"data/wcmc/variable/products_{count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                if product['type'] == 'variable':
                    db_product = await self._save_product(product)
                    if db_product:
                        print("variable product saved: ", db_product.name, " - ", db_product.id)
                        filename = f"data/wcmc/variations/variations_{product['id']}.json"
                        if os.path.exists(filename):
                            with open(filename, 'r') as f:
                                variations = json.load(f)
                            for variation in variations:
                                variation['name'] = product['name']+" - "+variation['name']
                                variation['parent_id'] = product['id']
                                variation['categories'] = product['categories']
                                variation['images'] = [variation['image']] if variation['image'] else []
                                variation['slug'] = product['slug'] + '-' + variation['name']
                                variation['featured'] = product['featured']
                                
                                variation_product = await self._save_product(variation)
                                if variation_product:
                                    print("Variation product saved: ", variation_product.name, " - ", variation_product.id)
                        success_count += 1
                        total_count += 1
                    else:
                        failed_products.append(product)
                        failed_count += 1
            
            count += 1
        
        print(f"Final totals - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
        return total_count
    
    async def get_orders(self):
        try:
            orders = []
            page = 1
            per_page = 100
            current_file_number = 1
            orders_per_file = 100
            
            while True:
                try:
                    page_orders = await self.wcmc.get_orders(per_page, page)
                    if not page_orders:  # If we get an empty response, we've reached the end
                        break
                    orders.extend(page_orders)
                    while len(orders) >= orders_per_file:
                        filename = f"data/wcmc/orders/orders_{current_file_number}.json"
                        batch = orders[:orders_per_file]
                        orders = orders[orders_per_file:]
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(batch, f, indent=4, ensure_ascii=False)
                        
                        print(f"Saved {filename}")
                        current_file_number += 1
                    page += 1
                except Exception as e:
                    print(f"Error on page {page}: {str(e)}")
                    return {"error": str(e), "last_successful_page": page - 1}
            
                if orders:  # Save any remaining products
                    filename = f"data/wcmc/orders/orders_{current_file_number}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(orders, f, indent=4, ensure_ascii=False)
                        print(f"Saved {filename}")
                        
                    return {
                        "success": True,
                        "message": f"Orders saved to data/wcmc/orders/orders_1.json through data/wcmc/orders/orders_{current_file_number}.json"
                    }
        except Exception as e:
            return {"error": f"Fatal error: {str(e)}"}
    
    async def _save_order(self, order_data):
        """Helper method to create and save an order and its line items"""
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
        
        try:
            # Save the order first
            db_order = await self.postgres.insert_order(order_base)
            if not db_order:
                return False, order_base
            
            # Save each line item
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
            return False, order_base

    async def create_orders(self):
        count = 1
        total_count = success_count = failed_count = 0
        failed_orders = []
        while True:
            if not os.path.exists(f"data/wcmc/orders/orders_{count}.json"):
                break
            
            with open(f"data/wcmc/orders/orders_{count}.json", "r") as f:
                orders = json.load(f)
                
            for order in orders:
                print(f"Processing order {order['id']}")
                success, failed_order = await self._save_order(order)
                if success:
                    success_count += 1
                else:
                    failed_orders.append(failed_order)
                    failed_count += 1
                total_count += 1
                
            print(f"Orders file {count} - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
            count += 1
        
        print(f"Final totals - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
        return total_count
    
    async def get_customers(self):
        page = 1
        per_page = 100
        customers = []
        current_file_number = 1
        customers_per_file = 100
        
        while True:
            page_customers = await self.wcmc.get_customers(per_page, page)
            if not page_customers:  # If no more customers are returned
                break
            
            customers.extend(page_customers)
            
            # Write to file every 100 customers
            while len(customers) >= customers_per_file:
                filename = f"data/wcmc/customers/customers_{current_file_number}.json"
                batch = customers[:customers_per_file]
                customers = customers[customers_per_file:]
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(batch, f, indent=4, ensure_ascii=False)
                
                print(f"Saved {filename}")
                current_file_number += 1
            
            page += 1
        
        # Write any remaining customers
        if customers:
            filename = f"data/wcmc/customers/customers_{current_file_number}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(customers, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")
            
        return f"Customers saved to customers_1.json through customers_{current_file_number}.json"
    
    async def _save_customer(self, customer_data):
        """Helper method to create and save a customer"""
        customer_base = CustomerBase(
            woo_id=customer_data["id"],
            first_name=customer_data["first_name"],
            last_name=customer_data["last_name"],
            username=customer_data["username"],
            email=customer_data["email"],
            billing_first_name=customer_data["billing"]["first_name"],
            billing_last_name=customer_data["billing"]["last_name"],
            billing_company=customer_data["billing"]["company"],
            billing_address_1=customer_data["billing"]["address_1"],
            billing_address_2=customer_data["billing"]["address_2"],
            billing_city=customer_data["billing"]["city"],
            billing_postcode=customer_data["billing"]["postcode"],
            billing_country=customer_data["billing"]["country"],
            billing_state=customer_data["billing"]["state"],
            billing_email=customer_data["billing"]["email"],
            billing_phone=customer_data["billing"]["phone"],
            shipping_first_name=customer_data["shipping"]["first_name"],
            shipping_last_name=customer_data["shipping"]["last_name"],
            shipping_company=customer_data["shipping"]["company"],
            shipping_address_1=customer_data["shipping"]["address_1"],
            shipping_address_2=customer_data["shipping"]["address_2"],
            shipping_city=customer_data["shipping"]["city"],
            shipping_postcode=customer_data["shipping"]["postcode"],
            shipping_country=customer_data["shipping"]["country"],
            shipping_state=customer_data["shipping"]["state"],
            shipping_phone=customer_data["shipping"]["phone"],
            is_paying_customer=customer_data["is_paying_customer"],
            avatar_url=customer_data["avatar_url"],
            created_at=customer_data["date_created"],
            updated_at=customer_data["date_modified"]
        )
        
        try:
            db_customer = await self.postgres.insert_customer(customer_base)
            return db_customer
        except Exception as e:
            print(f"Error inserting customer: {e}")
            return False
    
    async def create_customers(self):
        count = 1
        total_count = success_count = failed_count = 0
        failed_customers = []
        while True:
            if not os.path.exists(f"data/wcmc/customers/customers_{count}.json"):
                break
            
            with open(f"data/wcmc/customers/customers_{count}.json", "r") as f:
                customers = json.load(f)
                
            for customer in customers:
                db_customer = await self._save_customer(customer)
                if db_customer:
                    success_count += 1
                else:
                    failed_customers.append(customer)
                    failed_count += 1
                total_count += 1
                
            print(f"Customers level {count} - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
            count += 1
        
        print(f"Final totals - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
        return total_count
    
