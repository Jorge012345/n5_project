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

## Authentication

### Generating Access Tokens

The API uses Bearer Token authentication for secure access. Each police officer is associated with an access token which needs to be generated and included in the headers of POST requests.

#### Generating a Token via API

To generate an access token, make a POST request to the `/auth/token` endpoint with the officer's ID. Here is an example using `curl`:

```sh
curl -X POST "http://localhost:8000/dev/auth/token" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{"officer_id": "officer_1234"}'
```


## AWS Architecture Proposal

For deploying this application in production, the following AWS services are recommended:

1. **AWS Lambda:**
   - Used to run the FastAPI application without managing servers. It scales automatically and you only pay for the compute time you consume.

2. **Amazon API Gateway:**
   - Provides a secure endpoint to invoke the Lambda functions. It handles all the tasks associated with accepting and processing up to hundreds of thousands of concurrent API calls, including traffic management, authorization and access control, monitoring, and API version management.

3. **Amazon DynamoDB:**
   - A fully managed NoSQL database service that provides fast and predictable performance with seamless scalability. It’s used to store all the application data such as persons, vehicles, officers, and infractions.

4. **AWS Secrets Manager:**
   - Helps you protect access to your applications, services, and IT resources without the upfront cost and complexity of managing your own hardware security module (HSM) infrastructure. It’s used to securely store the `SECRET_KEY` for JWT token generation.

5. **Amazon CloudWatch:**
   - Provides monitoring for AWS cloud resources and applications. It can be used to collect and track metrics, collect and monitor log files, and set alarms.

6. **Amazon S3:**
   - Used for static file storage if needed (e.g., storing documentation, logs, etc.)

### Justification

- **AWS Lambda** is ideal for running the FastAPI application as it abstracts the server management and scales automatically with demand.
- **Amazon API Gateway** integrates seamlessly with Lambda and provides robust features for managing API calls, including throttling, logging, and security.
- **Amazon DynamoDB** offers a highly scalable and low-latency solution for database needs, which is crucial for a responsive API.
- **AWS Secrets Manager** ensures sensitive information such as the `SECRET_KEY` is stored securely and is easily accessible by the application.
- **Amazon CloudWatch** provides comprehensive monitoring and logging capabilities, which are essential for maintaining and troubleshooting the application in production.
- **Amazon S3** is a versatile service that can be used for storing various types of static assets required by the application.

By leveraging these AWS services, the application can achieve high availability, scalability, and security, ensuring a robust production deployment.


## Additional Information

- The API documentation is available at `/docs` once the server is running.
- The OpenAPI schema is available at `/openapi.json`.