Receipt Processor
=================

Overview
--------

This project implements a web service for processing receipts and calculating points based on a specific ruleset from the [Fetch Rewards Receipt Processor Challenge](https://github.com/fetch-rewards/receipt-processor-challenge).

The service is built using FastAPI and includes endpoints for submitting receipts and retrieving points awarded for a given receipt ID. The project is designed to fulfill the requirements of a coding challenge, with a focus on in-memory data storage, efficient request handling, and comprehensive testing.

## Challenge Requirements Met

- **Efficient Request Handling**: Utilizes FastAPI's async capabilities for efficient request handling.
- **In-Memory Storage**: Stores receipt data in memory, ensuring no data persistence across application restarts.
- **Comprehensive Testing**: Includes both unit and integration tests to ensure the correctness of the implementation.
- **Dockerized Setup**: Provides a Dockerfile for easy containerization and deployment.

## Unique Implementation Details

- **Singleton Pattern for ReceiptStore**: Ensures the same instance of `ReceiptStore` is used across all requests without using global variables.
- **Custom Exception Handlers**: Provides custom exception handlers for `ValidationError` and `HTTPException` to return meaningful error responses.
- **Custom Exception Handlers**: Provides custom exception handlers for `ValidationError` and `HTTPException` to return meaningful error responses.

API Endpoints
-------------

### 1.  Process Receipts

*   **Endpoint**: `/receipts/process`
*   **Method**: `POST`
*   **Description**: Submits a receipt for processing and returns a JSON object with an ID generated by the application.
*   **Request Body**: JSON object representing the receipt.
*   **Response**: JSON object containing the receipt ID.

#### Example Request

    json
    {
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
      ],
      "total": "35.35"
    }

#### Example Response

    {
      "id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
    }

### 2.  Get Points

*   **Endpoint**: `/receipts/{id}/points`
*   **Method**: `GET`
*   **Description**: Retrieves the points awarded for the receipt with the given ID.
*   **Response**: JSON object containing the number of points awarded.

#### Example Request

    GET /receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points

#### Example Response

    {
      "points": 28
    }

Points Calculation Rules
------------------------

1.  One point for every alphanumeric character in the retailer name.
2.  50 points if the total is a round dollar amount with no cents.
3.  25 points if the total is a multiple of 0.25.
4.  5 points for every two items on the receipt.
5.  If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer.
6.  6 points if the day in the purchase date is odd.
7.  10 points if the time of purchase is after 2:00pm and before 4:00pm.

Running the Application via Docker
-----------------------
Installation
------------

### Clone the repository

    git clone https://github.com/ryanlevee/receipt-processor.git
    

Make sure you are in the root directory for the project (`receipt-processor`).

### Build Docker image

    docker build -t receipt-processor-image:1.0 .
    

### Verify Docker image was successfully built

    docker images
    

### Run a container using the image

    docker run -d --name receipt-processor -p 8000:8000 receipt-processor-image:1.0
    

### Verify the container is running

    docker ps
    

### Verify the web service has started

    docker logs receipt-processor
    

API documentation can now be accessed at `http://localhost:8000/docs`.


### Running Tests

1.  Run the tests using pytest:
    
        pytest
        
    

Project Structure
-----------------

    receipt-processor/
    ├── main.py                # Main application code
    ├── tests/
    │   ├── __init__.py        # Test package initializer
    │   ├── test_integration.py# Integration tests
    │   ├── test_unit.py       # Unit tests
    ├── requirements.txt       # Project dependencies
    ├── Dockerfile             # Dockerfile for containerization
    └── README.md              # Project documentation
    

Running the Application Locally
----------------------------------------

1.  Clone the repository:
    
        git clone <repository-url>
        cd receipt-processor
        
    
2.  Install dependencies:
    
        pip install -r requirements.txt
        
    
3.  Run the application:
    
        uvicorn main:app --host 0.0.0.0 --port 8000
        
    
4.  Access the API documentation at `http://localhost:8000/docs`.
    
