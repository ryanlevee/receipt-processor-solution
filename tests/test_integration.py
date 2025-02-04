from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_process_receipt_target():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "total": "35.35",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
        ]
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_points_target():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "total": "35.35",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
        ]
    }
    process_response = client.post("/receipts/process", json=receipt)
    receipt_id = process_response.json()["id"]

    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    assert points_response.json()["points"] == 28


def test_process_receipt_target_single_item():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "total": "1.25",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
        ]
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_points_target_single_item():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "total": "1.25",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
        ]
    }
    process_response = client.post("/receipts/process", json=receipt)
    receipt_id = process_response.json()["id"]
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    expected_points = 31
    assert points_response.json()["points"] == expected_points


def test_process_receipt_walgreens():
    receipt = {
        "retailer": "Walgreens",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "08:13",
        "total": "2.65",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            {"shortDescription": "Dasani", "price": "1.40"}
        ]
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_points_walgreens():
    receipt = {
        "retailer": "Walgreens",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "08:13",
        "total": "2.65",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            {"shortDescription": "Dasani", "price": "1.40"}
        ]
    }
    process_response = client.post("/receipts/process", json=receipt)
    receipt_id = process_response.json()["id"]
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    expected_points = 15
    assert points_response.json()["points"] == expected_points
