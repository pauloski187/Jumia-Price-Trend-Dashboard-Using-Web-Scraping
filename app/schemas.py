from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: Optional[str] = None
    name: str
    price: float
    currency: Optional[str] = None
    url: Optional[str] = None


class PredictionRequest(BaseModel):
    features: dict


class PredictionResponse(BaseModel):
    prediction: float
