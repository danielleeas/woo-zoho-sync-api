from fastapi import APIRouter, Request

from app.agents.zoho import ZohoAgent
from app.agents.postgres import PostgresAgent

zoho_router = APIRouter(prefix="/oauth", tags=["OAuth"])

@zoho_router.get("/callback")
async def oauth_callback(request: Request):
    code = request.query_params.get('code')
    if not code:
        return {"error": "No code provided"}
    
    print(f"Code: {code}")
    
    response = await ZohoAgent().get_access_and_refresh_token(code)
    
    await PostgresAgent().insert_oauth(response.get("access_token"), response.get("refresh_token"), response.get("expires_at"))
    
    if response.get("error"):
        return {"error": response.get("error")}
    
    return {"access_token": response.get("access_token"), "refresh_token": response.get("refresh_token"), "expires_at": response.get("expires_at")}