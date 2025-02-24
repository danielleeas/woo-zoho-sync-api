import json, os
from app.agents.zoho import ZohoAgent

class ItemService:
    def __init__(self):
        self.zoho_agent = ZohoAgent()
        
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
