from datetime import datetime
from fastapi import APIRouter,Depends,Header,Query,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.connection import get_db
from app.core.security import current_user,require_admin
from app.models.order_item_model import OrderItem
from app.schemas.order_schema import OrderCreate,OrderOutput,OrderPage,StatusUpdate,ItemOutput
from app.services import order_service
router=APIRouter(prefix="/api/orders",tags=["Orders"])
def get_token(value):
    if not value or not value.lower().startswith("bearer "): raise HTTPException(401,"Bearer token required")
    return value.split(" ",1)[1].strip()
@router.post("/",response_model=OrderOutput,status_code=201)
async def create(data:OrderCreate,authorization:str|None=Header(None),user=Depends(current_user),db:Session=Depends(get_db)):
    return await order_service.create(db,data,user,get_token(authorization))
@router.get("/",response_model=OrderPage)
def list_all(page:int=Query(1,ge=1),page_size:int=Query(10,ge=1,le=100),status:str|None=None,
 date_from:datetime|None=None,date_to:datetime|None=None,user=Depends(current_user),db:Session=Depends(get_db)):
    return order_service.listing(db,user,page,page_size,status,date_from,date_to)
@router.get("/number/{order_number}",response_model=OrderOutput)
def number(order_number:str,user=Depends(current_user),db:Session=Depends(get_db)):
    return order_service.by_number(db,order_number,user)
@router.get("/{order_id}/items",response_model=list[ItemOutput])
def items(order_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    order_service.get_owned(db,order_id,user)
    return db.scalars(select(OrderItem).where(OrderItem.order_id==order_id)).all()
@router.get("/{order_id}",response_model=OrderOutput)
def one(order_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    return order_service.get_owned(db,order_id,user)
@router.patch("/{order_id}/status",response_model=OrderOutput)
def status(order_id:int,data:StatusUpdate,admin=Depends(require_admin),db:Session=Depends(get_db)):
    return order_service.set_status(db,order_id,data.order_status,admin)
@router.post("/{order_id}/cancel",response_model=OrderOutput)
async def cancel(order_id:int,authorization:str|None=Header(None),user=Depends(current_user),db:Session=Depends(get_db)):
    return await order_service.cancel(db,order_id,user,get_token(authorization))
