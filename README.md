# Traffic Violations API

## Overview
This is a FastAPI-based server for managing traffic violations. The server is built using FastAPI and is designed to run on AWS using Serverless Framework. This example demonstrates how to build a robust, scalable, and secure API for managing traffic violations.

## Requirements
- Python 3.9+
- Docker
- AWS CLI
- Serverless Framework

## Usage

### Local Development
To run the server locally, please execute the following from the root directory:

1. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Run the FastAPI server:
    ```sh
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

3. Open your browser and navigate to:
    ```
    http://localhost:8000/docs
    ```
    Here you can view and interact with your API using the Swagger UI.

### Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

1. Build the Docker image:
    ```sh
    docker build -t traffic-violations-api .
    ```

2. Start a Docker container:
    ```sh
    docker run -p 8000:8000 traffic-violations-api
    ```

3. Open your browser and navigate to:
    ```
    http://localhost:8000/docs
    ```
    Here you can view and interact with your API using the Swagger UI.

### Deployment to AWS

This project uses the Serverless Framework to deploy the API to AWS Lambda and API Gateway.

1. Install the Serverless Framework:
    ```sh
    npm install -g serverless
    ```

2. Configure your AWS credentials:
    ```sh
    serverless config credentials --provider aws --key YOUR_AWS_ACCESS_KEY --secret YOUR_AWS_SECRET_KEY
    ```

3. Deploy the service:
    ```sh
    serverless deploy
    ```

4. The deployment output will provide the URL to access your API. You can open your browser and navigate to the provided URL followed by `/dev/docs` to view and interact with your API using the Swagger UI.

## Project Structure
n5_project/
├── .serverless/
├── src/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── init.py
│   │   │   ├── auth.py
│   │   │   ├── infraction.py
│   │   │   ├── officer.py
│   │   │   ├── person.py
│   │   │   └── vehicle.py
│   │   ├── services/
│   │   │   ├── init.py
│   │   │   ├── auth.py
│   │   │   ├── infraction.py
│   │   │   ├── officer.py
│   │   │   ├── person.py
│   │   │   └── vehicle.py
│   │   ├── config.py
│   │   ├── schemas.py
│   │   └── init.py
├── .gitignore
├── README.md
├── requirements.txt
├── serverless.yml
└── main.py
└── Dockerfile

## Additional Information

- The API documentation is available at `/docs` once the server is running.
- The OpenAPI schema is available at `/openapi.json`.