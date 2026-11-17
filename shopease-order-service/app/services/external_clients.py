import httpx
from fastapi import HTTPException
from app.core.config import settings
class Clients:
    def __init__(self, token): self.headers={"Authorization":f"Bearer {token}"}
    async def request(self, method, url, **kwargs):
        try:
            async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
                response=await client.request(method,url,headers=self.headers,**kwargs)
            if response.status_code==404: raise HTTPException(404,"External resource not found")
            if response.status_code==409: raise HTTPException(409,"External service rejected inventory operation")
            response.raise_for_status()
            return response.json() if response.content else {}
        except HTTPException: raise
        except httpx.TimeoutException: raise HTTPException(504,"External service timed out")
        except httpx.HTTPStatusError: raise HTTPException(502,"External service returned an error")
        except httpx.RequestError: raise HTTPException(503,"External service unavailable")
    async def product(self,pid):
        p=await self.request("GET",f"{settings.PRODUCT_SERVICE_URL}/api/products/{pid}")
        if not p.get("is_active",True): raise HTTPException(400,f"Product {pid} is inactive")
        return p
    async def stock(self,pid,qty,direction,key):
        endpoint="stock-out" if direction=="OUT" else "stock-in"
        stock_headers={"Idempotency-Key":key}
        if settings.INVENTORY_SERVICE_TOKEN:
            stock_headers["Authorization"]=f"Bearer {settings.INVENTORY_SERVICE_TOKEN}"
        return await self.request("POST",f"{settings.PRODUCT_SERVICE_URL}/api/inventory/{pid}/{endpoint}",
            json={"quantity":qty,"remarks":f"Order operation {key}"},headers=stock_headers)
    async def address(self,address_id):
        data=await self.request("GET",f"{settings.USER_SERVICE_URL}/api/users/addresses/{address_id}")
        result=data.get("address",data.get("data",data))
        if not isinstance(result,dict): raise HTTPException(502,"Unexpected User Service address response")
        return result
