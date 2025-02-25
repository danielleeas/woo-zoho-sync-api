import os, json
from app.agents.postgres import PostgresAgent
from app.models.category import CategoryBase

class CRUDService:
    def __init__(self):
        self.postgres = PostgresAgent()
    
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
