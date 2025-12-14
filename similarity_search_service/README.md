# Similarity Search Service

This service is a core component of the [FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application](https://github.com/AchrefHemissi/FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application), responsible for intelligently matching lost and found items. It leverages advanced AI models and vector databases to perform similarity searches based on both textual and visual descriptions of items.

## Overview

The `similarity_search_service` is a modular FastAPI microservice designed for generating and searching image/text embeddings. It uses OpenAI's CLIP model to create embeddings from item descriptions and images, and then utilizes Qdrant, a high-performance vector similarity search engine, to find the most similar items. Additionally, it integrates with Neo4j, a graph database, which likely supports more complex relationship-based matching or data enrichment for improved accuracy.

## Key Features

*   **Image and Text Embedding Generation**: Converts diverse item descriptions (text and images) into numerical embeddings using OpenAI's CLIP model.
*   **Vector Similarity Search**: Efficiently finds similar items by comparing their embeddings using Qdrant.
*   **Neo4j Integration**: Enhances matching capabilities through graph-based relationships and data enrichment.
*   **FastAPI Framework**: Provides a robust and high-performance API for seamless integration with other services.
*   **Scalable and Production-Ready**: Designed for scalability to handle large volumes of lost and found reports and is suitable for production environments.

## Technologies Used

*   **Python**: The primary programming language.
*   **FastAPI**: Web framework for building the API.
*   **OpenAI CLIP**: For generating image and text embeddings.
*   **Qdrant**: Vector similarity search engine.
*   **Neo4j**: Graph database for relationship-based data.
*   **Docker**: For containerization.
*   **Docker Compose**: For multi-container application management.

## Project Structure

The service's internal structure is organized for clarity and maintainability:

*   `app/`: Contains the main application code.
    *   `main.py`: The entry point for the FastAPI application.
    *   `api/`: Defines the API endpoints.
        *   `v1/`, `v2/`: Different versions of the API for text/image embedding.
        *   `endpoints/`: Specific endpoint definitions (e.g., `embeddings.py`).
        *   `dependencies.py`: Shared dependencies like model loaders and database connections.
    *   `core/`: Core settings and configurations.
        *   `config.py`: Handles environment variables and application settings.
        *   `logger.py`: Configures application-wide logging.
    *   `services/`: Business logic implementations.
        *   `clip_service.py`: Manages CLIP model loading and embedding generation.
        *   `vector_service.py`: Handles operations with the vector database (Qdrant/FAISS).
    *   `models/`: Pydantic models for request and response data (e.g., `embedding_request.py`).
    *   `utils/`: Utility functions.
        *   `image_utils.py`: Contains image preprocessing functions for CLIP.
*   `tests/`: Unit and integration tests for the service.
*   `test_images/`: Sample images used for testing purposes.
*   `.env`: Environment variables for configuration.
*   `requirements.txt`: Lists all Python dependencies.
*   `README.md`: This project overview and instructions.

## Setup and Installation

To set up and run the `similarity_search_service` locally, follow these steps:

1.  **Clone the main repository**:

    ```bash
    git clone https://github.com/AchrefHemissi/lostfound-smart_matching-and-fraud_detection-microservices.git
    cd lostfound-smart_matching-and-fraud_detection-microservices/similarity_search_service
    ```

2.  **Environment Configuration**: Create a `.env` file in the `similarity_search_service` directory and configure necessary environment variables, such as API keys for OpenAI, and connection details for Qdrant and Neo4j. Refer to the service's internal documentation or code for specific variable names.

3.  **Build and Run with Docker Compose**:

    Navigate to the `similarity_search_service` directory and execute the following command:

    ```bash
    docker-compose up --build
    ```

    This command will:
    *   Build the Docker image for the service.
    *   Start the service container along with its dependencies, including Qdrant and Neo4j instances.

## Usage

Once the service is running, it will be accessible via its defined FastAPI endpoints. It is designed to receive requests for generating embeddings and performing similarity searches. It also interacts with RabbitMQ by consuming messages from `task_queue_similarity` and publishing results to `result_similarity_queue`, as depicted in the overall system architecture diagram.



