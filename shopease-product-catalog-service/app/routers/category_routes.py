from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import require_admin
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services import category_service

router = APIRouter(prefix="/api/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, status_code=201)
def create(data: CategoryCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return category_service.create_category(db, data.model_dump())

@router.get("/", response_model=list[CategoryResponse])
def list_all(db: Session = Depends(get_db)):
    return category_service.list_categories(db)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_one(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category(db, category_id)

@router.put("/{category_id}", response_model=CategoryResponse)
def update(category_id: int, data: CategoryCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return category_service.update_category(db, category_id, data.model_dump())

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(category_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    category_service.delete_category(db, category_id)
    return Response(status_code=204)