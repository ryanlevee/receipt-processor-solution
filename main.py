import logging
import math
import uuid
from datetime import datetime
from typing import Dict, List
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()


class ReceiptStore:
    def __init__(self):
        self.receipts: Dict[str, int] = {}

    def add_receipt(self, receipt_id: str, points: int):
        self.receipts[receipt_id] = points

    def get_points(self, receipt_id: str) -> int:
        return self.receipts.get(receipt_id)


receipt_store = ReceiptStore()


def get_receipt_store():
    return receipt_store


class Item(BaseModel):
    shortDescription: str = Field(
        ...,
        pattern=r"^[\w\s\-]+$",
        json_schema_extra={"example": "Mountain Dew 12PK"},
    )
    price: str = Field(
        ...,
        pattern=r"^\d+\.\d{2}$",
        json_schema_extra={"example": "6.49"}
    )


class Receipt(BaseModel):
    retailer: str = Field(
        ...,
        pattern=r"^[\w\s\-\&]+$",
        json_schema_extra={"example": "M&M Corner Market"},
    )
    purchaseDate: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        json_schema_extra={"example": "2022-01-01"},
    )
    purchaseTime: str = Field(
        ...,
        pattern=r"^\d{2}:\d{2}$",
        json_schema_extra={"example": "13:01"}
    )
    items: List[Item] = Field(..., min_length=1)
    total: str = Field(
        ...,
        pattern=r"^\d+\.\d{2}$",
        json_schema_extra={"example": "6.49"}
    )


def calc_points(receipt: Receipt) -> int:
    points: int = 0
    retailer: str = receipt.retailer
    total: float = float(receipt.total)
    purchase_date: str = receipt.purchaseDate
    purchase_time: str = receipt.purchaseTime
    items: List[Item] = receipt.items

    # Rule 1: One point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in retailer)

    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if total.is_integer():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt
    points += (len(items) // 2) * 5

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer
    for item in items:
        description: str = item.shortDescription.strip()
        price: float = float(item.price)
        if len(description) % 3 == 0:
            points += math.ceil(price * 0.2)

    # Rule 6: 6 points if the day in the purchase date is odd
    dt_purchase_date: datetime = datetime.strptime(purchase_date, "%Y-%m-%d")
    if dt_purchase_date.day % 2 != 0:
        points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    hour: int = int(purchase_time.split(":")[0])
    if 14 <= hour < 16:
        points += 10

    return points


@app.post("/receipts/process")
async def process_receipt(
    background_tasks: BackgroundTasks,
    receipt: Receipt,
    store: ReceiptStore = Depends(get_receipt_store),
):
    logger.info("Processing receipt: %s", receipt.model_dump_json())
    receipt_id: str = str(uuid.uuid4())
    points: int = calc_points(receipt)
    await store.add_receipt(receipt_id, points)
    logger.info(
        "Receipt processed with ID: %s and points: %d", receipt_id, points
    )

    background_tasks.add_task(log_receipt_processing, receipt_id, points)

    return {"id": receipt_id}


async def log_receipt_processing(receipt_id: str, points: int):
    # async with httpx.AsyncClient() as client:
        # await client.post(
        #     "http://example.com/log", json={"id": receipt_id, "points": points}
        # )
    logger.info({"id": receipt_id, "points": points})  # log_receipt_processing PLACEHOLDER


@app.get("/receipts/{id}/points")
async def get_points(
    id: str, store: ReceiptStore = Depends(get_receipt_store)
):
    logger.info("Fetching points for receipt ID: %s", id)
    points: int = await store.get_points(id)
    if points is not None:
        logger.info("Points for receipt ID %s: %d", id, points)
        return {"points": points}
    else:
        logger.error("No receipt found for ID: %s", id)
        raise HTTPException(
            status_code=404, detail="No receipt found for that ID."
        )


@app.exception_handler(ValidationError)
async def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    logger.error("Validation error: %s", exc.errors())
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.errors(),
            "message": "Invalid input data. Please verify input.",
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    logger.error("HTTP error: %s", exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
