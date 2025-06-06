# Python Data Fetcher

A Python project featuring a REST API server for handling numbers with concurrent access and an asynchronous API client for fetching URLs in parallel. The server uses FastAPI for efficient JSON handling, and the client uses `httpx` for async HTTP requests with retry logic.

## Project Overview

### REST API Server (`api_server.py`)
A FastAPI server with two endpoints:
- **POST /numbers**:
  - Accepts JSON payload: `{"number": int}`.
  - Stores numbers in memory with thread-safe concurrency using a `Lock`.
  - Example:
    ```bash
    curl -X POST "http://localhost:8000/numbers" -H "Content-Type: application/json" -d '{"number": 42}'
    ```
    Response:
    ```json
    {"status": "success", "number": 42}
    ```
- **GET /average**:
  - Returns the average of submitted numbers: `{"average": float}`.
  - Example:
    ```json
    {"average": 42.0}
    ```
  - Returns 404 if no numbers are submitted.

### Async API Client (`async_client.py`)
A script that:
- Reads URLs from `urls.json` (e.g., `{"urls": ["https://api.github.com", ...]}`).
- Fetches URLs asynchronously with up to 2 retries on failure.
- Outputs:
  - Total and successful response counts.
  - Total, fastest, slowest, and average response times.
  - Failed requests with errors.
- Example run:
    ```bash
    python async_client.py
    ```

## Prerequisites
- Python 3.9+
- curl or Postman (for testing)

## Setup Instructions
1. Clone the repository:
    ```bash
    git clone https://github.com/ArqamFarooq/python-data-fetcher.git
    cd python-data-fetcher
    ```
2. Install dependencies:
    ```bash
    pip install fastapi uvicorn httpx pydantic
    ```
3. Run the API server:
    ```bash
    python api_server.py
    ```
    Test with:
    ```bash
    curl -X POST "http://localhost:8000/numbers" -H "Content-Type: application/json" -d '{"number": 10}'
    curl "http://localhost:8000/average"
    ```
4. Run the async client:
    - Ensure `urls.json` exists.
    - Run:
        ```bash
        python async_client.py
        ```

## CI/CD Pipeline
A GitHub Actions workflow (`.github/workflows/ci.yml`) automates the following on push or pull requests to the `main` branch:
- **Linting**: Runs `flake8` to ensure code quality.
- **Testing**: Executes unit tests with `pytest` (if test files are added).
- **Building**: Builds the Docker image for the API server with `docker build -t python-fetcher:latest .`.
- **Optional Deployment**: Can deploy to a test Kubernetes namespace using Helm (not enabled).

View CI runs in the GitHub repository's Actions tab.

## Project Structure
```plaintext
├── api_server.py
├── async_client.py
├── urls.json
└── README.md
```

## Testing
Test the API:
```bash
curl -X POST "http://localhost:8000/numbers" -H "Content-Type: application/json" -d '{"number": 10}'
curl "http://localhost:8000/average"
```

## License
MIT License