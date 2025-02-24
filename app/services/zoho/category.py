import os, json
from app.agents.zoho import ZohoAgent
from app.agents.postgres import PostgresAgent
from app.models.category import CategoryBase

class ZohoCategoryService:
    def __init__(self):
        self.zoho_agent = ZohoAgent()
        self.postgres_agent = PostgresAgent()

    async def _create_and_save_category(self, category_data, parent_zoho_id="-1"):
        """Helper method to create and save a category"""
        category_base = CategoryBase(
            name=category_data["name"],
            woo_id=category_data["woo_id"],
            woo_parent_id=category_data["woo_parent_id"],
            description=category_data["description"],
            url=category_data["url"],
            zoho_id=None,
            zoho_parent_id=parent_zoho_id
        )
        
        result = await self.zoho_agent.create_category(category_base)
        if not result.get("category"):
            return False, category_data
            
        category_base.zoho_id = result['category']['category_id']
        category_base.zoho_parent_id = result['category']['parent_category_id']
        await self.postgres_agent.insert_category(category_base)
        depth_info = f" deep {self.current_depth}" if hasattr(self, 'current_depth') else ""
        print(f"Created category {category_data['name']} with id {category_base.zoho_id}{depth_info}")
        return True, None

    async def create_categories(self):
        """Create categories from JSON files"""
        self.current_depth = 1
        total_count = success_count = failed_count = 0
        failed_categories = []

        while True:
            filename = f"data/wcmc/categories_level_{self.current_depth}.json"
            if not os.path.exists(filename):
                break

            with open(filename, 'r') as f:
                categories = json.load(f)

            for category in categories:
                parent_zoho_id = "-1"
                if category["woo_parent_id"] != 0:
                    parent_category = await self.postgres_agent.get_category_by_woo_id(category["woo_parent_id"])
                    if parent_category:
                        parent_zoho_id = parent_category.zoho_id

                success, failed_category = await self._create_and_save_category(category, parent_zoho_id)
                if success:
                    success_count += 1
                else:
                    failed_categories.append(failed_category)
                    failed_count += 1
                total_count += 1

            print(f"Depth {self.current_depth} - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
            self.current_depth += 1

        # Handle failed categories
        if failed_categories:
            print(f"Failed categories: {failed_categories}")
            with open("data/wcmc/failed_categories.json", "w") as f:
                json.dump(failed_categories, f, indent=4, ensure_ascii=False)

        print(f"Final totals - Total: {total_count}, Success: {success_count}, Failed: {failed_count}")
        return "Categories created"
    
    async def create_category(self):
        """Create a category from JSON file"""
        json_data = {
            "name": "Vertikal spön (2)",
            "woo_id": 2666,
            "woo_parent_id": 823,
            "description": "",
            "url": "vertikal-spon-2"
        }
        
        parent_category = await self.postgres_agent.get_category_by_woo_id(json_data["woo_parent_id"])
        if parent_category:
            parent_zoho_id = parent_category.zoho_id
        else:
            parent_zoho_id = "-1"
        
        print(f"Parent category: {parent_zoho_id}")
            
        success, failed_category = await self._create_and_save_category(json_data, parent_zoho_id)
        
        print(f"Success: {success}")
        print(f"Failed category: {failed_category}")
        
        # filename = "data/wcmc/categories_level_1.json"
        # with open(filename, 'r') as f:
        #     categories = json.load(f)
        # return categories
        
        return "Category created"
