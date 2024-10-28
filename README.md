Here's a simplified `README.md` for your project, without Docker and with direct text examples:

---

# URL Shortener Service

## Overview
The URL Shortener Service is a web application built with FastAPI to generate shortened URLs for easy sharing and access. Users can shorten URLs, retrieve original URLs, and optionally set custom slugs and expiration times.

## Table of Contents
- Project Structure
- Getting Started
- API Endpoints
- Environment Variables
- Testing
- Design Decisions
- License

---

## Project Structure

- `server.py`: Contains the main FastAPI server and route definitions.
- `models.py`: Defines the data models and database schema.
- `services.py`: Core business logic for URL generation, retrieval, and analytics.
- `rate_limit.py`: Implements rate limiting functionality.
- `README.md`: Project documentation.

---

## Getting Started

### Prerequisites
Ensure you have:
- Python 3.9+

### Installation
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd url-shortener-service
   ```

2. **Set up the virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**: Refer to the [Environment Variables](#environment-variables) section.

5. **Run the application**:
   ```bash
   uvicorn server:app --reload
   ```

---

## API Endpoints

### 1. **POST /url/shorten**
   - **Description**: Shortens a given full URL.
   - **Input**: JSON payload with `url` key.
   - **Output**: JSON response with the `short_url` key.

   **Example**:
   ```
   Request:
   POST /url/shorten
   {
     "url": "https://www.example.com"
   }

   Response:
   {
     "short_url": "http://localhost:8000/r/abc123"
   }
   ```

### 2. **GET /r/{short_url}**
   - **Description**: Redirects to the original URL for a given shortened URL.
   - **Output**: HTTP 302 redirect or 404 if not found.

   **Example**:
   ```
   Request:
   GET /r/abc123

   Response:
   HTTP 302 Redirect to "https://www.example.com"
   ```

### Optional Endpoints
- **Custom Slugs**: Specify a custom slug in the `short_url` field when creating a shortened URL.
- **Analytics**: Track the number of accesses for each shortened URL.

---

## Environment Variables

Create a `.env` file in the root directory with the following:

```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379
RATE_LIMIT_ENABLED=True
RATE_LIMIT_WINDOW=60
RATE_LIMIT_COUNT=10
```

---

## Testing

### Running Tests
To ensure functionality, run unit tests for core functionalities:

1. **Run tests**:
   ```bash
   pytest
   ```

2. **Testing via Postman**:
   - Use a JSON payload for `/url/shorten`.
   - Verify redirect and 404 for `/r/{short_url}`.

---

## Design Decisions

1. **Data Persistence**: PostgreSQL ensures reliable data storage across instances.
2. **Concurrency**: Concurrency support allows for handling multiple requests using an appropriate database.
3. **Rate Limiting**: Redis enables efficient rate limiting, configurable via the `rate_limit.py` module.



