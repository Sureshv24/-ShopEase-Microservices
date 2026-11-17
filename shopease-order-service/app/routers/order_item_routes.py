from fastapi import APIRouter
# Order items are created atomically with the order and read through the order routes.
router=APIRouter(tags=["Order Items"])
