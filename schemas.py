from pydantic import BaseModel

# -------- VENDOR --------
class VendorCreate(BaseModel):
    name: str
    contact: str
    rating: float

class VendorResponse(VendorCreate):
    id: int

    class Config:
        from_attributes = True


# -------- PRODUCT --------
class ProductCreate(BaseModel):
    name: str
    sku: str
    unit_price: float
    stock_level: int

class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True

# -------- PO ITEMS --------
class POItem(BaseModel):
    product_id: int
    quantity: int
    price: float


# -------- CREATE PO --------
class PurchaseOrderCreate(BaseModel):
    reference_no: str
    vendor_id: int
    items: list[POItem]


# -------- RESPONSE --------
class PurchaseOrderResponse(BaseModel):
    id: int
    reference_no: str
    vendor_id: int
    total_amount: float
    status: str

    class Config:
        from_attributes = True


# -------- ITEM RESPONSE --------
class POItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


# -------- FULL PO RESPONSE --------
class PurchaseOrderFullResponse(BaseModel):
    id: int
    reference_no: str
    vendor_id: int
    total_amount: float
    status: str
    items: list[POItemResponse]

    class Config:
        from_attributes = True