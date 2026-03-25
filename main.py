from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

# Dependency (DB session)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- CREATE VENDOR ----------------
@app.post("/vendors", response_model=schemas.VendorResponse)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    new_vendor = models.Vendor(
        name=vendor.name,
        contact=vendor.contact,
        rating=vendor.rating
    )
    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor


# ---------------- GET VENDORS ----------------
@app.get("/vendors", response_model=list[schemas.VendorResponse])
def get_vendors(db: Session = Depends(get_db)):
    return db.query(models.Vendor).all()


# ---------------- CREATE PRODUCT ----------------
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=product.name,
        sku=product.sku,
        unit_price=product.unit_price,
        stock_level=product.stock_level
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# ---------------- GET PRODUCTS ----------------
@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

# ---------------- CREATE PURCHASE ORDER ----------------
@app.post("/purchase-orders", response_model=schemas.PurchaseOrderResponse)
def create_po(po: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):

    # Step 1: Calculate total
    total = 0
    for item in po.items:
        total += item.quantity * item.price

    tax = total * 0.05
    final_total = total + tax

    # Step 2: Create PO
    new_po = models.PurchaseOrder(
        reference_no=po.reference_no,
        vendor_id=po.vendor_id,
        total_amount=final_total,
        status="CREATED"
    )

    db.add(new_po)
    db.commit()
    db.refresh(new_po)

    # Step 3: Add items
    for item in po.items:
        po_item = models.PurchaseOrderItem(
            po_id=new_po.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(po_item)

    db.commit()

    return new_po

# ---------------- GET ALL PURCHASE ORDERS ----------------
@app.get("/purchase-orders", response_model=list[schemas.PurchaseOrderFullResponse])
def get_purchase_orders(db: Session = Depends(get_db)):
    return db.query(models.PurchaseOrder).all()