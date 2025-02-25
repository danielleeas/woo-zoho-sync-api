import httpx, json
import http.client
from datetime import datetime, timedelta

from app.config import settings
from app.agents.postgres import PostgresAgent
from app.models.category import CategoryBase

class ZohoAgent:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.client_id = settings.ZOHO_CLIENT_ID
        self.client_secret = settings.ZOHO_CLIENT_SECRET
        self.redirect_uri = settings.ZOHO_REDIRECT_URI
        self.postgres_agent = PostgresAgent()
    
    async def get_access_and_refresh_token(self, code: str):
        async with httpx.AsyncClient() as client:
            print(settings.ZOHO_CLIENT_ID)
            response = await client.post(
                "https://accounts.zoho.eu/oauth/v2/token",
                data={
                    "code": code,
                    "client_id": settings.ZOHO_CLIENT_ID,
                    "client_secret": settings.ZOHO_CLIENT_SECRET,
                    "redirect_uri": settings.ZOHO_REDIRECT_URI,
                    "grant_type": "authorization_code"
                }
            )
        
        response_data = response.json()
        
        print(response_data)
        
        if response.status_code != 200:
            return {"error": response_data}
        
        try:
            self.access_token = response_data["access_token"]
            self.refresh_token = response_data["refresh_token"]
            self.expires_at = datetime.now() + timedelta(seconds=response_data["expires_in"])
        except Exception as e:
            return {"error": str(e)}

        return {"access_token": self.access_token, "refresh_token": self.refresh_token, "expires_at": self.expires_at}
    
    async def get_access_token_from_refresh_token(self, refresh_token: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://accounts.zoho.eu/oauth/v2/token",
                data={
                    "refresh_token": refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                    "grant_type": "refresh_token"
                }
            )
        
        response_data = response.json()
        
        print(response_data)
        
        if response.status_code != 200:
            return {"error": response_data}
        
        self.access_token = response_data["access_token"]
        self.expires_at = datetime.now() + timedelta(seconds=response_data["expires_in"])
        
        result = await self.postgres_agent.update_oauth(self.access_token, refresh_token, self.expires_at)
        
        if not result:
            return {"error": "Failed to update OAuth token"}
        
        return result
    
    async def get_access_token(self):
        try:
            oauth_token = await self.postgres_agent.get_oauth()
            
            if not oauth_token:
                return {"error": "No OAuth token available"}
            
            if oauth_token.expires_at < datetime.now():
                new_oauth_token = await self.get_access_token_from_refresh_token(oauth_token.refresh_token)
                if "error" in new_oauth_token:
                    return {"error": new_oauth_token["error"]}
                oauth_token = new_oauth_token
                
            return oauth_token.access_token
        except Exception as e:
            return {"error": f"Error retrieving access token: {str(e)}"}
    
    async def get_items(self, page: int = 1, per_page: int = 100):
        try:
            access_token = await self.get_access_token()
            if isinstance(access_token, dict) and "error" in access_token:
                return access_token

            conn = http.client.HTTPSConnection("www.zohoapis.eu")
            headers = {'Authorization': f"Zoho-oauthtoken {access_token}"}
            
            try:
                print(f"Getting items from page {page} with per_page {per_page}")
                conn.request("GET", f"/inventory/v1/items?organization_id={settings.ZOHO_ORGANIZATION_ID}&page={page}&per_page={per_page}", headers=headers)
                res = conn.getresponse()
                data = res.read()
                json_data = json.loads(data.decode('utf-8'))
                return json_data
            except http.client.HTTPException as e:
                print(f"HTTP connection error: {str(e)}")
                return {"error": f"HTTP connection error: {str(e)}"}
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                return {"error": f"JSON decode error: {str(e)}"}
            finally:
                conn.close()
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    async def adjust_stock(self, item_id: int, quantity: float):
        try:
            access_token = await self.get_access_token()
            if isinstance(access_token, dict) and "error" in access_token:
                return access_token
            
            conn = http.client.HTTPSConnection("www.zohoapis.eu")
            headers = {
                'Authorization': f"Zoho-oauthtoken {access_token}",
                'Content-Type': 'application/json'
            }
            
            try:
                payload = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "reason": "Stock Adjustment",
                    "adjustment_type": "quantity",
                    "line_items": [
                        {
                            "item_id": item_id,
                            "quantity_adjusted": quantity,
                        }
                    ]
                }
                
                # Convert payload to JSON string and encode to bytes
                json_payload = json.dumps(payload).encode('utf-8')
                
                conn.request("POST", f"/inventory/v1/inventoryadjustments?organization_id={settings.ZOHO_ORGANIZATION_ID}", json_payload, headers)
                res = conn.getresponse()
                data = res.read()
                json_data = json.loads(data.decode('utf-8'))
                return json_data
            except http.client.HTTPException as e:
                print(f"HTTP connection error: {str(e)}")
                return {"error": f"HTTP connection error: {str(e)}"}
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                return {"error": f"JSON decode error: {str(e)}"}
            finally:
                conn.close()
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    async def create_category(self, category: CategoryBase):
        access_token = await self.get_access_token()
            
        conn = http.client.HTTPSConnection("www.zohoapis.eu")
        
        payload = json.dumps({
            "name": category.name,
            "url": category.url,
            "parent_category_id": category.zoho_parent_id
        })

        headers = { 'Authorization': f"Zoho-oauthtoken {access_token}" }

        conn.request("POST", f"/inventory/v1/categories?organization_id={settings.ZOHO_ORGANIZATION_ID}", payload, headers)

        res = conn.getresponse()
        data = res.read()
        json_data = data.decode('utf-8')  # Convert bytes to string
        print(json_data)
        return json.loads(json_data)
    
    async def get_taxes(self):
        access_token = await self.get_access_token()
        
        conn = http.client.HTTPSConnection("www.zohoapis.eu")
        
        headers = { 'Authorization': f"Zoho-oauthtoken {access_token}" }
        
        conn.request("GET", f"/inventory/v1/settings/taxes?organization_id={settings.ZOHO_ORGANIZATION_ID}", headers=headers)
        
        res = conn.getresponse()
        data = res.read()
        json_data = data.decode('utf-8')  # Convert bytes to string
        return json.loads(json_data)
