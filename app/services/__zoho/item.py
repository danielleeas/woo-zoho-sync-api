import json, os

from app.agents.zoho import ZohoAgent
from app.agents.postgres import PostgresAgent
from app.schemas.item import Item

class ItemService:
    def __init__(self):
        self.zoho_agent = ZohoAgent()
        self.postgres_agent = PostgresAgent()
        
    async def items_json(self):
        page = 1
        per_page = 100  # Items per page
        file_number = 0
        
        try:
            while True:
                try:
                    result = await self.zoho_agent.get_items(page, per_page)
                except Exception as e:
                    print(f"Error fetching items from Zoho on page {page}: {str(e)}")
                    break

                # Check if we have items in the response
                if 'items' not in result or not result['items']:
                    print(f"No items found in the response")
                    break
                    
                try:
                    # Save current batch to a JSON file
                    filename = f"data/zoho/items/items_{file_number}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(result['items'], f, indent=4, ensure_ascii=False)
                except IOError as e:
                    print(f"Error saving items to file {filename}: {str(e)}")
                    break
                    
                print(f"Saved batch {file_number} with {len(result['items'])} items to {filename}")
                
                # Check if we've reached the last page
                if len(result['items']) < per_page:
                    break
                    
                page += 1
                file_number += 1
                
            print(f"Successfully saved {file_number} batches of items")
            return {"message": "Items fetched successfully"}
            
        except Exception as e:
            print(f"Unexpected error occurred: {str(e)}")
    
    async def update_items(self):
        total_updated = 0
        count = 0
        while True:
            print(f"Processing batch {count}")
            filename = f"data/zoho/items/items_{count}.json"
            if not os.path.exists(filename):
                print(f"File {filename} does not exist")
                break
            
            with open(filename, "r") as f:
                items = json.load(f)
            
            print(f"Processing {len(items)} items")
            for item in items:
                try:
                    if item["stock_on_hand"] > 0:
                        item_data = {
                            "item_id": item["item_id"],
                            "quantity": -item["stock_on_hand"],
                        }
                        print(item_data)
                        await self.zoho_agent.adjust_stock(**item_data)
                        total_updated += 1
                except KeyError as e:
                    print(f"Missing required field in item data: {str(e)}")
                    continue
                except Exception as e:
                    print(f"Unexpected error processing item: {str(e)}")
                    continue
            
            count += 1
        
        print(f"Total items updated: {total_updated}")
    
    async def make_upload_items_list(self):
        items = []
        api_count = 0
        api_count_limit = 8348
        count = 1
        file_number = 0
        
        while True:
            filename = f"data/wcmc/final/products_{count}.json"
            if not os.path.exists(filename):
                print(f"File {filename} does not exist")
                break
            
            with open(filename, "r") as f:
                products = json.load(f)
            
            for product in products:
                api_length = len(product["images"]) + 1
                api_count += api_length
                if api_count >= api_count_limit:
                    break
                    
                items.append(product)
                
                # Save every 100 items
                if len(items) >= 100:
                    output_filename = f"data/sync/items/items_{file_number}.json"
                    with open(output_filename, 'w', encoding='utf-8') as f:
                        json.dump(items, f, indent=4, ensure_ascii=False)
                    print(f"Saved {output_filename} with {len(items)} items")
                    items = []  # Reset items list
                    file_number += 1
            
            if api_count >= api_count_limit:
                break
            
            count += 1
        
        # Save any remaining items
        if items:
            output_filename = f"data/sync/items/items_{file_number}.json"
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=4, ensure_ascii=False)
            print(f"Saved {output_filename} with {len(items)} items")
    
    async def json_taxs(self):
        result = await self.zoho_agent.get_taxes()
        taxes = []
    
        for tax in result['taxes']:
            taxes.append({
                'id': tax['tax_id'],
                'name': tax['tax_name'],
                'rate': tax['tax_percentage']
            })
        
        with open('data/taxes.json', 'w') as f:
            json.dump(taxes, f, indent=4, ensure_ascii=False)
      
    async def create_items(self):
        count = 0
        total_count = 0
        successful_syncs = 0
        errors = []
        limit_exceeded = False
        
        while True:
            if limit_exceeded:
                break
            
            try:
                filename = "data/sync/items/items_{count}.json"
                with open(filename, 'r') as f:
                    products = json.load(f)
                
                total_products = len(products)
                print(f"Starting sync of {total_products} products")
                
                for product in products:
                    if limit_exceeded:
                        print("API limit exceeded. Stopping sync.")
                        break
                        
                    try:
                        # Get category
                        category_id = "-1"
                        if product["categories"]:
                            category_woo_id = product["categories"][0]["id"]
                            category = await self.postgres_agent.get_category_by_woo_id(category_woo_id)
                            if category:
                                category_id = category.zoho_id
                        
                        # Get brand
                        brand = product["brands"][0]["name"] if product["brands"] else "Eagle Fishing"
                        
                        # Process stock
                        try:
                            stock_qty = max(0.0, float(product["stock_quantity"]))
                        except (ValueError, TypeError):
                            stock_qty = 0.0
                        
                        available_stock = stock_qty if product["stock_status"] == "instock" else 0.0
                        
                        # Process price
                        try:
                            price = float(product["price"]) if product["price"] else 0.0
                        except (ValueError, TypeError):
                            price = 0.0
                            
                        # Create item
                        item_base = Item(
                            name=product["name"],
                            item_name=product["name"],
                            category_id=category_id,
                            unit="pcs",
                            status="active",
                            description=product["description"],
                            brand=brand,
                            manufacturer=brand,
                            rate=price,
                            tax_id="721775000000054249",
                            initial_stock=stock_qty,
                            stock_on_hand=stock_qty,
                            available_stock=available_stock,
                            actual_available_stock=available_stock,
                            purchase_rate=price,
                            item_type="inventory",
                            product_type="goods",
                            sku=product["sku"],
                            length=product["dimensions"]["length"],
                            width=product["dimensions"]["width"],
                            height=product["dimensions"]["height"],
                            weight=product["weight"],
                            weight_unit="kg",
                            dimension_unit="cm"
                        )
                        
                        # Create item in Zoho
                        result = await self.zoho_agent.create_item(item_base)
                        print(result)
                        if result.get("limit_exceeded"):
                            limit_exceeded = True
                            break
                        
                        # Handle image upload
                        if result.get("item") and product["images"]:
                            try:
                                await self.zoho_agent.upload_image(product["images"], result['item']['item_id'])
                                print(f"Uploaded {len(product['images'])} images for {product['name']}")
                            except Exception as e:
                                errors.append(f"Image upload error for {product['name']}: {str(e)}")
                        
                        successful_syncs += 1
                        total_count += 1
                        
                        # Progress update every 10 items
                        if total_count % 10 == 0:
                            print(f"Progress: {total_count}/{total_products} ({(total_count/total_products)*100:.1f}%)")
                    
                    except Exception as e:
                        errors.append(f"Product error - {product.get('name', 'unknown')}: {str(e)}")
                        continue
                
                count += 1
                
            except Exception as e:
                errors.append(f"File error - {filename}: {str(e)}")
        
        print(f"Total count: {total_count}")
        if errors:
            print("\nErrors encountered:")
            for error in errors:
                print(f"- {error}")
