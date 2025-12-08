from fastapi import APIRouter
from .schemas import Product, PredictionRequest, PredictionResponse

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/products", response_model=Product)
def create_product(product: Product):
    # Placeholder implementation
    return product


@router.post("/predict", response_model=PredictionResponse)
def predict_price(req: PredictionRequest):
    # Placeholder prediction
    return PredictionResponse(prediction=0.0)
