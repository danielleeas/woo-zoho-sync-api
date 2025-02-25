import os, json
import unicodedata
from bs4 import BeautifulSoup

from app.agents.wcmc import WCMC
from app.agents.postgres import PostgresAgent
from app.models.category import CategoryBase
from app.models.product import ProductBase

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
            price=product_data["price"],
            regular_price=product_data["regular_price"],
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
                    print("variable product saved: ", db_product.name, " - ", db_product.id)
                    if db_product:
                        filename = f"data/wcmc/variations/variations_{product['id']}.json"
                        if os.path.exists(filename):
                            with open(filename, 'r') as f:
                                variations = json.load(f)
                            for variation in variations:
                                variation['name'] = product['name']+" - "+variation['name']
                                variation['parent_id'] = db_product.id
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
                        failed_products.append(variation)
                        failed_count += 1
            
            count += 1
        
        print(f"Final totals - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
        return total_count
                
