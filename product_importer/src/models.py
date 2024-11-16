from datetime import datetime, timezone
from typing import List
from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    stock_code: str
    color: List[str]
    discounted_price: float
    images: List[str]
    is_discounted: bool
    name: str
    price: float
    price_unit: str
    product_type: str
    quantity: int
    sample_size: str
    series: str
    status: str
    fabric: str
    model_measurements: str
    product_measurements: str
    createdAt: datetime = datetime.now(timezone.utc)
    updatedAt: datetime = datetime.now(timezone.utc)
