from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload
from app.core.config import settings
from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.services.external_clients import Clients
def money(v): return Decimal(v).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
def get_owned(db,oid,user):
    o=db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id==oid))
    if not o: raise HTTPException(404,"Order not found")
    if user["role"] not in {"admin","administrator"} and o.user_id!=user["user_id"]:
        raise HTTPException(403,"You cannot access another user's order")
    return o
async def create(db,data,user,token):
    ext=Clients(token); address=await ext.address(data.shipping_address_id)
    quantities={}
    for item in data.items: quantities[item.product_id]=quantities.get(item.product_id,0)+item.quantity
    products={}
    for pid,qty in quantities.items():
        p=await ext.product(pid)
        if int(p.get("stock_quantity",0))<qty: raise HTTPException(409,f"Insufficient stock for product {pid}")
        products[pid]=p
    subtotal=Decimal("0"); discount=Decimal("0"); rows=[]
    for pid,qty in quantities.items():
        p=products[pid]; regular=Decimal(str(p["price"])); sale=Decimal(str(p.get("discount_price") or p["price"]))
        d=money((regular-sale)*qty); line=money(sale*qty)
        subtotal+=money(regular*qty); discount+=d
        rows.append(dict(product_id=pid,product_name=p["name"],sku=p.get("sku",str(pid)),
            unit_price=sale,quantity=qty,discount_amount=d,total_price=line))
    subtotal=money(subtotal); discount=money(discount); net=money(subtotal-discount)
    shipping=Decimal("0.00") if net>=settings.FREE_SHIPPING_THRESHOLD else settings.SHIPPING_CHARGE
    tax=money(net*settings.TAX_RATE); total=money(net+tax+shipping)
    number="SHP-"+datetime.utcnow().strftime("%Y%m%d")+"-"+uuid4().hex[:10].upper()
    order=Order(order_number=number,user_id=user["user_id"],shipping_address=address,
        subtotal=subtotal,discount_amount=discount,shipping_charge=shipping,tax_amount=tax,total_amount=total,
        order_status="PENDING",payment_status="PENDING",notes=data.notes)
    reserved=[]
    try:
        for pid,qty in quantities.items():
            key=f"reserve:{number}:{pid}"
            await ext.stock(pid,qty,"OUT",key); reserved.append((pid,qty,key))
        db.add(order); db.flush()
        for row in rows: db.add(OrderItem(order_id=order.id,**row))
        db.commit()
        return get_owned(db,order.id,user)
    except Exception:
        db.rollback()
        for pid,qty,key in reversed(reserved):
            try: await ext.stock(pid,qty,"IN",f"compensate:{key}")
            except Exception: pass
        raise
def listing(db,user,page,size,status,date_from,date_to):
    q=select(Order).options(selectinload(Order.items)); cq=select(func.count(Order.id))
    if user["role"] not in {"admin","administrator"}:
        q=q.where(Order.user_id==user["user_id"]); cq=cq.where(Order.user_id==user["user_id"])
    if status:
        q=q.where(Order.order_status==status.upper()); cq=cq.where(Order.order_status==status.upper())
    if date_from: q=q.where(Order.created_at>=date_from); cq=cq.where(Order.created_at>=date_from)
    if date_to: q=q.where(Order.created_at<=date_to); cq=cq.where(Order.created_at<=date_to)
    total=db.scalar(cq) or 0
    rows=db.scalars(q.order_by(Order.created_at.desc()).offset((page-1)*size).limit(size)).all()
    return {"total":total,"page":page,"page_size":size,"items":rows}
def by_number(db,number,user):
    o=db.scalar(select(Order).options(selectinload(Order.items)).where(Order.order_number==number))
    if not o: raise HTTPException(404,"Order not found")
    if user["role"] not in {"admin","administrator"} and o.user_id!=user["user_id"]: raise HTTPException(403,"Forbidden")
    return o
def set_status(db,oid,new,user):
    o=get_owned(db,oid,user)
    transitions={"PENDING":{"CONFIRMED","CANCELLED"},"CONFIRMED":{"PROCESSING","CANCELLED"},
      "PROCESSING":{"SHIPPED","CANCELLED"},"SHIPPED":{"DELIVERED"},"DELIVERED":set(),"CANCELLED":set()}
    if new not in transitions.get(o.order_status,set()): raise HTTPException(409,f"Invalid transition {o.order_status} -> {new}")
    o.order_status=new; o.updated_at=datetime.utcnow(); db.commit(); db.refresh(o)
    return get_owned(db,oid,user)
async def cancel(db,oid,user,token):
    o=get_owned(db,oid,user)
    if o.order_status=="CANCELLED": return o
    if o.order_status not in {"PENDING","CONFIRMED","PROCESSING"}: raise HTTPException(409,"Order cannot be cancelled after shipment")
    o=db.scalar(select(Order).where(Order.id==oid).with_for_update())
    if o.order_status=="CANCELLED": return get_owned(db,oid,user)
    if o.order_status not in {"PENDING","CONFIRMED","PROCESSING"}: raise HTTPException(409,"Order is no longer cancellable")
    key=o.cancellation_key or f"cancel:{o.order_number}"; o.cancellation_key=key; db.commit()
    ext=Clients(token); items=db.scalars(select(OrderItem).where(OrderItem.order_id==oid)).all()
    try:
        for item in items: await ext.stock(item.product_id,item.quantity,"IN",f"{key}:{item.product_id}")
        o=db.get(Order,oid); o.order_status="CANCELLED"; o.updated_at=datetime.utcnow(); db.commit()
        return get_owned(db,oid,user)
    except Exception:
        db.rollback()
        raise HTTPException(502,"Stock restoration failed; reconcile inventory operation before retrying")
