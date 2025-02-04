import pytest

from main import Item, Receipt, calc_points


@pytest.mark.asyncio
async def test_calc_points_target():
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-01-01",
        purchaseTime="13:01",
        total="35.35",
        items=[
            Item(shortDescription="Mountain Dew 12PK", price="6.49"),
            Item(shortDescription="Emils Cheese Pizza", price="12.25"),
            Item(shortDescription="Knorr Creamy Chicken", price="1.26"),
            Item(shortDescription="Doritos Nacho Cheese", price="3.35"),
            Item(shortDescription="Klarbrunn 12-PK 12 FL OZ", price="12.00")
        ]
    )
    points = calc_points(receipt)
    assert points == 28


@pytest.mark.asyncio
async def test_calc_points_round_total_MM():
    receipt = Receipt(
        retailer="M&M Corner Market",
        purchaseDate="2022-03-20",
        purchaseTime="14:33",
        total="9.00",
        items=[
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25")
        ]
    )
    points = calc_points(receipt)
    assert points == 109


@pytest.mark.asyncio
async def test_calc_points_walgreens():
    receipt = Receipt(
        retailer="Walgreens",
        purchaseDate="2022-01-02",
        purchaseTime="08:13",
        total="2.65",
        items=[
            Item(shortDescription="Pepsi - 12-oz", price="1.25"),
            Item(shortDescription="Dasani", price="1.40")
        ]
    )
    points = calc_points(receipt)
    expected_points = 15
    assert points == expected_points


@pytest.mark.asyncio
async def test_calc_points_target_single_item():
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-01-02",
        purchaseTime="13:13",
        total="1.25",
        items=[
            Item(shortDescription="Pepsi - 12-oz", price="1.25")
        ]
    )
    points = calc_points(receipt)
    expected_points = 31
    assert points == expected_points
