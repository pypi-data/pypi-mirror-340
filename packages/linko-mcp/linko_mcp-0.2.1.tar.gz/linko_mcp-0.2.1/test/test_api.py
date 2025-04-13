import asyncio
from linko_mcp.api_client import LinkoAPIClient
from linko_mcp import auth

async def test_api():
    client = LinkoAPIClient()
    # Test authentication
    token_data = auth.get_stored_token()
    if token_data:
        print("Token found:", bool(token_data))
    
    # Test API call
    try:
        response = await client.get("/api/note/")
        print("API call successful:", bool(response))
    except Exception as e:
        print("API call failed:", e)
    
    await client.close()

asyncio.run(test_api())