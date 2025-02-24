import json
from app.agents.wcmc import WCMC

class CategoryService:
    def __init__(self):
        self.wcmc_agent = WCMC()

    async def category_json(self):
        total_categories = []
        page = 1
        while True:
            categories = await self.wcmc_agent.get_categories(page=page)
            if not categories:
                break
            
            total_categories.extend(categories)
            page += 1
        with open("data/wcmc/categories.json", "w") as f:
            json.dump(total_categories, f, indent=4)
        
        print(f"Total categories: {len(total_categories)}")
        return total_categories
    
    async def clear_categories(self):
        
        clear_categories = []
        with open("data/wcmc/categories.json", "r") as f:
            categories = json.load(f)
        
        for category in categories:
            category.pop('_links', None)
            category.pop('yoast_head', None)
            category.pop('yoast_head_json', None)
            clear_categories.append(category)
        
        with open("data/wcmc/categories_cleared.json", "w") as f:
            json.dump(clear_categories, f, indent=4)
        
        print("Categories cleared")
        
        return "Categories cleared"
    
    async def separate_categories(self):
        # Read the file using async with
        categories = None
        with open("data/wcmc/categories_cleared.json", "r") as f:
            categories = json.load(f)
            
        if not categories:
            return "No categories found"
            
        # Create a dictionary to store categories by their levels
        categories_by_level = {}
        
        # Helper function to determine category level
        def get_category_level(category, all_categories):
            level = 0
            current_cat = category
            while current_cat["parent"] != 0:
                level += 1
                # Find parent category
                parent = next((cat for cat in all_categories if cat["id"] == current_cat["parent"]), None)
                if parent is None:
                    break
                current_cat = parent
            return level
        
        # Group categories by their levels
        for category in categories:
            try:
                level = get_category_level(category, categories)
                if level not in categories_by_level:
                    categories_by_level[level] = []
                    
                categories_by_level[level].append({
                    "name": category["name"],
                    "woo_id": category["id"],
                    "woo_parent_id": category["parent"],
                    "description": category["description"],
                    "url": category["slug"]
                })
            except Exception as e:
                print(f"Error processing category {category['name']}: {str(e)}")
                continue
        
        # Save categories for each level
        for level, cats in categories_by_level.items():
            filename = f"data/wcmc/categories_level_{level}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(cats, f, indent=4, ensure_ascii=False)
            
        return f"Categories separated by levels and saved to categories_level_[0-{max(categories_by_level.keys())}].json"
