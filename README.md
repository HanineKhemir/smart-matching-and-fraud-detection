# Lost & Found Smart Matching and Fraud Detection Microservices

A microservices-based backend system for intelligent lost-and-found item matching and suspicious user detection. Part of the **FoundIT** platform - a Computer Vision Powered Lost and Found Mobile Application.

## Overview

This project consists of two independent microservices:

| Service | Purpose |
|---------|---------|
| **Similarity Search Service** | Matches lost and found items using AI-powered image/text embeddings |
| **Suspicious User Detection Service** | Detects fraudulent users and suspicious activities using LLM agents |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FoundIT Platform                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────┐    ┌─────────────────────────────────┐ │
│  │  Similarity Search Service  │    │ Suspicious User Detection Svc  │ │
│  │                             │    │                                 │ │
│  │  ┌─────────┐ ┌───────────┐  │    │  ┌──────────┐ ┌──────────────┐  │ │
│  │  │  CLIP   │ │  Qdrant   │  │    │  │ LangChain│ │    Redis     │  │ │
│  │  │ Model   │ │ Vector DB │  │    │  │  Agent   │ │    Cache     │  │ │
│  │  └─────────┘ └───────────┘  │    │  └──────────┘ └──────────────┘  │ │
│  │       │           │         │    │       │             │           │ │
│  │       └─────┬─────┘         │    │       └──────┬──────┘           │ │
│  │             │               │    │              │                  │ │
│  │       ┌─────▼─────┐         │    │        ┌─────▼─────┐            │ │
│  │       │   Neo4j   │         │    │        │  Llama    │            │ │
│  │       │ Graph DB  │         │    │        │  3.2 LLM  │            │ │
│  │       └───────────┘         │    │        └───────────┘            │ │
│  └─────────────────────────────┘    └─────────────────────────────────┘ │
│                                                                          │
│  Message Queues (RabbitMQ):                                              │
│  • task_queue_similarity → result_similarity_queue                       │
│  • task_queue_suspicious → result_suspicious_queue                       │
└─────────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| AI/ML | PyTorch, OpenAI CLIP (ViT-B/32) |
| LLM | LangChain + Llama 3.2-8B |
| Vector Database | Qdrant |
| Graph Database | Neo4j |
| Cache | Redis |
| Containerization | Docker |
| Image Processing | PIL, imagehash |

## Project Structure

```
├── similarity_search_service/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── api/
│   │   │   ├── v1/endpoints/       # API v1 routes
│   │   │   └── v2/endpoints/       # API v2 routes
│   │   ├── services/
│   │   │   ├── clip_service.py     # CLIP embedding generation
│   │   │   └── vector_service.py   # Qdrant operations
│   │   ├── repositories/
│   │   │   └── neo4j_repository.py # Graph DB operations
│   │   ├── models/
│   │   │   └── embedding_request.py
│   │   └── config/
│   │       ├── config.py           # Environment config
│   │       ├── qdrant_config.py    # Vector DB setup
│   │       └── neo4j_config.py     # Graph DB setup
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── suspicious_user_detection_service/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── api/
│   │   │   ├── v1/endpoints/       # API v1 routes
│   │   │   └── v2/endpoints/       # API v2 routes
│   │   ├── services/
│   │   │   ├── scam_detector_agent.py  # LLM-based detection
│   │   │   └── agent_tools.py      # Detection tools
│   │   ├── repositories/
│   │   │   └── redis_repo.py       # Redis operations
│   │   ├── models/
│   │   │   ├── anomaly.py          # Request/response models
│   │   │   └── scam_state.py       # Detection state
│   │   └── config/
│   │       ├── config.py           # Environment config
│   │       └── redis_client.py     # Redis setup
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── README.md
```

## Services

### 1. Similarity Search Service

Intelligently matches lost and found items using semantic embeddings.

**Features:**
- CLIP-based 512-dimensional embeddings from images and text
- Cosine similarity search with Qdrant vector database
- Automatic filtering (lost items match with found items)
- Graph-based relationship tracking in Neo4j

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v2/embedding/generate` | Generate and store embeddings |
| GET | `/api/v2/embedding/similar/{post_id}` | Find similar items |
| DELETE | `/api/v2/embedding/delete` | Remove embeddings |

**How it works:**
1. User uploads an image with description
2. CLIP model generates semantic embedding
3. Embedding stored in Qdrant with metadata
4. On search, finds similar items with opposite post type (lost ↔ found)
5. Matches recorded in Neo4j as `SIMILAR_TO` relationships

### 2. Suspicious User Detection Service

Detects fraudulent users using pattern detection and LLM analysis.

**Features:**
- Duplicate image detection (perceptual hashing)
- External link tracking
- Post frequency anomaly detection
- LLM-powered behavioral analysis
- Confidence scoring with recommendations

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v2/anomalydetection/detect` | Analyze user for suspicious activity |

**Detection Methods:**
1. **Duplicate Images** - Detects reused images across posts using perceptual hashing
2. **External Links** - Flags posts containing external URLs
3. **Post Frequency** - Detects 3+ posts in a single day
4. **LLM Analysis** - Analyzes content for scam indicators:
   - Inconsistent story details
   - Urgent personal info requests
   - Pressure tactics
   - Unusual reward mentions

**Scoring:**
- Each detected pattern adds +1 to suspicious score
- Score >= 3 triggers user flagging
- Response includes confidence level and recommendations (flag/monitor/ignore)

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Access to required services:
  - OpenAI API (or compatible proxy)
  - Neo4j database
  - Redis instance
  - Qdrant (included in docker-compose)

### Environment Variables

Create `.env` files in each service directory:

**Both Services:**
```env
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://api.openai.com/v1
PROXY_API_KEY=your_proxy_key
PROXY_BASE_URL=your_proxy_url
```

**Similarity Search Service:**
```env
NEO4J_URI=neo4j+s://your-neo4j-instance
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

**Suspicious User Detection Service:**
```env
REDIS_PASSWORD=your_redis_password
```

### Running with Docker

**Similarity Search Service:**
```bash
cd similarity_search_service
docker-compose up --build
```
Service runs on `http://localhost:8000`

**Suspicious User Detection Service:**
```bash
cd suspicious_user_detection_service
docker-compose up --build
```
Service runs on `http://localhost:8000`

### Running Locally

```bash
# Similarity Search Service
cd similarity_search_service
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Suspicious User Detection Service
cd suspicious_user_detection_service
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## API Usage Examples

### Generate Embedding (Similarity Search)

```bash
curl -X POST "http://localhost:8000/api/v2/embedding/generate" \
  -F "post_id=123" \
  -F "post_type=lostitem" \
  -F "item_type=electronics" \
  -F "text=Lost black iPhone 14 near Central Park" \
  -F "image=@/path/to/image.jpg"
```

### Find Similar Items

```bash
curl "http://localhost:8000/api/v2/embedding/similar/123"
```

### Detect Suspicious User

```bash
curl -X POST "http://localhost:8001/api/v2/anomalydetection/detect" \
  -F "user_id=user123" \
  -F 'posts=[{"postid":"p1","date":"2024-01-15","posttype":"found","text":"Found wallet with $500","itemtype":"wallet"}]' \
  -F "image=@/path/to/image.jpg"
```

## Message Queue Integration

For production deployment, services integrate with RabbitMQ:

```
Gateway → task_queue_similarity → Similarity Service → result_similarity_queue
Gateway → task_queue_suspicious → Detection Service → result_suspicious_queue
```

## Configuration Details

### Qdrant Vector Database
- Embedding dimension: 512
- Distance metric: Cosine
- Index: HNSW (m=16, ef_construct=100)

### Redis Cache
- TTL for image hashes: 30 days
- TTL for link counters: 30 days
- TTL for daily post counters: 24 hours

### LLM Configuration
- Model: llama3-8b-8192
- Temperature: 0 (deterministic)
- Structured output with JSON schema validation

## License

This project is part of the FoundIT platform.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
