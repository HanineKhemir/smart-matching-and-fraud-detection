# Suspicious User Detection Service

This service is part of the [FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application](https://github.com/AchrefHemissi/FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application)
, specifically designed to identify and flag suspicious user activities and potentially fraudulent reports. It plays a crucial role in maintaining the integrity and security of the platform by analyzing user behavior and report patterns.

## Overview

The `suspicious_user_detection_service` is a microservice that consumes messages related to user activities and reports. It processes this information to detect anomalies that might indicate fraudulent behavior or suspicious patterns. The service leverages **Redis** for efficient data storage and retrieval, which is essential for real-time analysis and quick flagging of suspicious entities.

## Key Features

*   **Real-time Anomaly Detection**: Processes incoming user data and reports to identify unusual activities as they occur.
*   **Integration with Redis**: Utilizes Redis for fast access to user profiles, historical data, and blacklists, enabling rapid fraud checks.
*   **Scalable Architecture**: Designed as a microservice, allowing it to scale independently based on the load and complexity of detection tasks.

## Technologies Used

*   **Python**: The primary programming language for the service logic.
*   **Redis**: Used as a high-performance in-memory data store for caching and quick lookups.
*   **Docker**: For containerization, ensuring consistent deployment across different environments.
*   **Docker Compose**: For defining and running multi-container Docker applications, simplifying the setup of the service and its dependencies.

## Setup and Installation

To get the `suspicious_user_detection_service` up and running, follow these steps:

1.  **Clone the main repository**:

    ```bash
    git clone https://github.com/AchrefHemissi/lostfound-smart_matching-and-fraud_detection-microservices.git
    cd lostfound-smart_matching-and-fraud_detection-microservices/suspicious_user_detection_service
    ```

2.  **Environment Configuration**: Ensure you have a `.env` file or equivalent environment variables configured for any necessary credentials or settings (e.g., Redis connection details). While not explicitly detailed in the public repository, this is a common practice for microservices.

3.  **Build and Run with Docker Compose**:

    Navigate to the `suspicious_user_detection_service` directory and execute the following command:

    ```bash
    docker-compose up --build
    ```

    This command will:
    *   Build the Docker image for the service.
    *   Start the service container along with its dependencies, such as a Redis instance.

## Usage

Once the service is running, it will listen for messages from the RabbitMQ `task_queue_suspicious` (as indicated in the overall system architecture). It will process these messages, perform its detection logic, and then send results back to the `result_suspicious_queue` for the Gateway to consume.



