import json, os
import unicodedata
from bs4 import BeautifulSoup

from app.agents.wcmc import WCMC

class ProductService:
    def __init__(self):
        self.wcmc = WCMC()
        
    async def all_products(self):
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
        
    async def get_product(self, product_id: int):
        product = await self.wcmc.get_product(product_id)
        return product
    
    async def delete_products(self):
        product = await self.wcmc.delete_product(116481)
        return product
    
    async def clear_products(self):
        cleaned_products = []
        count = 1
        products_per_file = 100
        current_file_number = 1
        while True:
            
            if not os.path.exists(f"data/wcmc/simple/products_{count}.json"):
                break
            
            with open(f"data/wcmc/simple/products_{count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                if product["name"] == "Produkt":
                    continue
                product.pop('meta_data', None)
                product.pop('yoast_head', None)
                product.pop('price_html', None)
                product.pop('yoast_head_json', None)
                cleaned_products.append(product)
                while len(cleaned_products) >= products_per_file:
                    filename = f"data/wcmc/cleaned/products_{current_file_number}.json"
                    batch = cleaned_products[:products_per_file]
                    cleaned_products = cleaned_products[products_per_file:]
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(batch, f, indent=4, ensure_ascii=False)
                    
                    print(f"Saved {filename}")
                    current_file_number += 1
                
            count += 1
        if cleaned_products:
            filename = f"data/wcmc/cleaned/products_{current_file_number}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(cleaned_products, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")
        
        print(f"Products cleaned and saved to products_1.json through products_{current_file_number}.json")
        return {"success": True, "message": "Products cleaned successfully"}
    
    async def clear_products_description(self):
        described_products = []
        count = 1
        products_per_file = 100
        current_file_number = 1
        while True:
            if not os.path.exists(f"data/wcmc/cleaned/products_{count}.json"):
                break
            
            with open(f"data/wcmc/cleaned/products_{count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                final_description = ""
                if product["description"] or product["short_description"]:
                    text = product["description"] or product["short_description"]
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
                    
                product['description'] = final_description if final_description != "" else "No Description"
                described_products.append(product)
                
                while len(described_products) >= products_per_file:
                    filename = f"data/wcmc/described/products_{current_file_number}.json"
                    batch = described_products[:products_per_file]
                    described_products = described_products[products_per_file:]
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(batch, f, indent=4, ensure_ascii=False)
                    
                    print(f"Saved {filename}")
                    current_file_number += 1
            
            count += 1
        
        if described_products:
            filename = f"data/wcmc/described/products_{current_file_number}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(described_products, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")
        
        print(f"Products described and saved to products_1.json through products_{current_file_number}.json")
        return {"success": True, "message": "Products described successfully"}
    
    async def check_null_sku(self):
        null_sku_products = []
        count = 1
        while True:
            if not os.path.exists(f"data/wcmc/described/products_{count}.json"):
                break
            
            with open(f"data/wcmc/described/products_{count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                if product["sku"] == "":
                    null_sku_products.append(product)
            count += 1
            
        if null_sku_products:
            filename = f"data/wcmc/null_sku/null_sku_products.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(null_sku_products, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")
            
        return {"success": True, "message": "Products with null SKU saved to products_1.json through products_{count}.json"}
    
    async def search_duplicate_sku(self):
        duplicate_sku_list = []
        count = 1
        sku_list = []
        unique_sku_products = []
        while True:
            if not os.path.exists(f"data/wcmc/described/products_{count}.json"):
                break
            
            with open(f"data/wcmc/described/products_{count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                if product['sku'] in sku_list:
                    duplicate_sku_list.append(product['sku'])
                else:
                    sku_list.append(product['sku'])
            count += 1
        
        duplicate_sku_products = []
        new_count = 1
        while True:
            if not os.path.exists(f"data/wcmc/described/products_{new_count}.json"):
                break
            
            with open(f"data/wcmc/described/products_{new_count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                if product['sku'] in duplicate_sku_list:
                    duplicate_sku_products.append(product)
                else:
                    unique_sku_products.append(product)
            new_count += 1
            
        
        if duplicate_sku_products:
            filename = f"data/wcmc/duplicate_sku/duplicate_sku_products.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(duplicate_sku_products, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")
            
        if unique_sku_products:
            products_per_file = 100
            current_file_number = 1
            
            while len(unique_sku_products) >= products_per_file:
                filename = f"data/wcmc/unique_sku/products_{current_file_number}.json"
                batch = unique_sku_products[:products_per_file]
                unique_sku_products = unique_sku_products[products_per_file:]
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(batch, f, indent=4, ensure_ascii=False)
                print(f"Saved {filename}")
                current_file_number += 1
            
            # Save any remaining products
            if unique_sku_products:
                filename = f"data/wcmc/unique_sku/products_{current_file_number}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(unique_sku_products, f, indent=4, ensure_ascii=False)
                print(f"Saved {filename}")
            
        return f"Duplicate SKUs saved to duplicate_sku_products_{new_count}.json"
    
    async def search_duplicate_name(self):
        duplicate_name_list = []
        count = 1
        name_list = []
        while True:
            if not os.path.exists(f"data/wcmc/described/products_{count}.json"):
                break
            
            with open(f"data/wcmc/described/products_{count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                print(product['name'])
                if product['name'] in name_list:
                    duplicate_name_list.append(product['name'])
            count += 1
        
        duplicate_name_products = []
        new_count = 1
        while True:
            if not os.path.exists(f"data/wcmc/described/products_{new_count}.json"):
                break
            
            with open(f"data/wcmc/described/products_{new_count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                if product['name'] in duplicate_name_list:
                    duplicate_name_products.append(product)
            new_count += 1
        
        if duplicate_name_products:
            filename = f"data/wcmc/duplicate_name/duplicate_name_products.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(duplicate_name_products, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")
            
        return f"Duplicate Names saved to duplicate_name_products.json"
    
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
    
    async def check_no_variations(self):
        count = 1
        no_variations = []
        while True:
            if not os.path.exists(f"data/wcmc/variable/products_{count}.json"):
                break
            
            with open(f"data/wcmc/variable/products_{count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                
                filename = f"data/wcmc/variations/variations_{product['id']}.json"
                if not os.path.exists(filename):
                    no_variations.append(product)
            count += 1
            
        if no_variations:
            filename = f"data/wcmc/no_variations/no_variations.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(no_variations, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")
            
        return f"No Variations saved"
    
    async def count_variations(self):
        count = 0
        for filename in os.listdir('data/wcmc/variations'):
            if filename.startswith('variations_') and filename.endswith('.json'):
                count += 1
        
        return {"total_variation_files": count}
    
    async def check_duplicated_sku_variations(self):
        sku_list = []
        duplicate_sku_list = []
        
        # Iterate through all variation files in the variations directory
        for filename in os.listdir('data/wcmc/variations'):
            if not filename.startswith('variations_') or not filename.endswith('.json'):
                continue
                
            filepath = f"data/wcmc/variations/{filename}"
            with open(filepath, "r") as f:
                variations = json.load(f)
                
            # Check each variation's SKU
            for variation in variations:
                if variation['sku'] in sku_list:
                    duplicate_sku_list.append(variation)
                else:
                    sku_list.append(variation['sku'])
        
        # Save duplicate SKUs to a file if any found
        if duplicate_sku_list:
            filename = "data/wcmc/duplicate_sku/duplicate_sku_variations.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(duplicate_sku_list, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")
        
        parent_ids = []
        for variation in duplicate_sku_list:
            if variation['parent_id'] not in parent_ids:
                parent_ids.append(variation['parent_id'])
        
        parent_products = []
        count = 1
        while True:
            if not os.path.exists(f"data/wcmc/variable/products_{count}.json"):
                break
            
            with open(f"data/wcmc/variable/products_{count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                if product['id'] in parent_ids:
                    parent_products.append(product)
            count += 1
        
        if parent_products:
            filename = f"data/wcmc/parent_products/parent_products.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(parent_products, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")
            
        return {
            "success": True,
            "total_skus": len(sku_list),
            "duplicate_count": len(duplicate_sku_list),
            "message": "Duplicate variation SKUs have been saved"
        }
    
    async def check_duplicated_name_variable_products(self):
        count = 1
        products_names = []
        duplicate_products_names = []
        while True:
            if not os.path.exists(f"data/wcmc/variable/products_{count}.json"):
                break
            
            with open(f"data/wcmc/variable/products_{count}.json", "r") as f:
                products = json.load(f)
            
            for product in products:
                if product['name'] in products_names:
                    duplicate_products_names.append(product['name'])
                else:
                    products_names.append(product['name'])
                    
            count += 1
        
        new_count = 1
        while True:
            if not os.path.exists(f"data/wcmc/cleaned/cleaned_products_{new_count}.json"):
                break
            
            with open(f"data/wcmc/cleaned/cleaned_products_{new_count}.json", "r") as f:
                products = json.load(f)
                
            for product in products:
                if product['name'] in duplicate_products_names:
                    duplicate_products_names.append(product)
                else:
                    products_names.append(product['name'])
            new_count += 1
        
        if duplicate_products_names:
            filename = f"data/wcmc/duplicate_name/duplicate_products_names.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(duplicate_products_names, f, indent=4, ensure_ascii=False)
            print(f"Saved {filename}")