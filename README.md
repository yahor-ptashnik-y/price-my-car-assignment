# Price My Car API - Candidate Assignment

This project is an implementation of the "Price My Car" API assignment. It is a REST API built with FastAPI that takes a car's title and description, uses a Large Language Model (LLM) via LangChain to extract its make and model, and returns an estimated price.

You can run this project by following the [local setup instructions](#getting-started-local-setup) or test the [live deployed version](#deployment) directly.

---

## Features

-   **Intelligent Extraction**: Uses **OpenAI's GPT model** via **LangChain** to reliably extract structured `make` and `model` data from unstructured text.
-   **REST API Endpoint**: A `POST /price-car` endpoint that accepts car listing details.
-   **Pricing Tool Integration**: Connects to a simulated Python tool (`get_car_price`) to retrieve a price estimate.
-   **Robust Error Handling**: Gracefully handles potential errors, such as LLM extraction failures or unknown vehicle models, returning clear error messages with appropriate HTTP status codes.
-   **Interactive API Docs**: Provides automatically generated, interactive API documentation (via Swagger UI) to easily test the endpoint.
-   **Secure & Asynchronous**: Follows best practices by using environment variables for API keys and leveraging asynchronous processing for high performance.

---

## Tech Stack

-   **Framework**: FastAPI
-   **LLM Framework**: LangChain
-   **LLM Provider**: OpenAI
-   **Production Server**: Gunicorn
-   **Development Server**: Uvicorn
-   **Language**: Python 3.9+

---

## Getting Started (Local Setup)

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

-   Python 3.9 or newer
-   An OpenAI API key

### 2. Setup Instructions

**Step 1: Clone the repository**

```sh
git clone git@github.com:yahor-ptashnik-y/price-my-car-assignment.git
cd price-my-car-assignment
```

**Step 2: Create and activate a virtual environment**

Using a virtual environment is highly recommended to keep project dependencies isolated.

-   **On macOS/Linux:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
-   **On Windows:**
    ```sh
    python -m venv venv
    .\\venv\\Scripts\\activate
    ```

**Step 3: Set up your environment variables**

The application requires an OpenAI API key to function.

1.  Create a file named `.env` in the root of your project.
2.  Open the `.env` file and add your OpenAI API key like this:

    ```
    # .env
    OPENAI_API_KEY="sk-..."
    ```

**Step 4: Install dependencies**

Install all the required Python packages, including `gunicorn` for production.

```sh
pip install -r requirements.txt
```

---

## Running the Application Locally

For local development, start the API server with Uvicorn.

```sh
uvicorn main:app
```

The server will start and listen on `http://127.0.0.1:8000`.

Add `--reload` flag that enables hot-reloading, which automatically restarts the server when you make changes to the code.

```sh
uvicorn main:app --reload
```

---

## How to Use the API

You can test the API using the interactive documentation or a tool like `cURL`.

### Option A: Using the Interactive Docs (Recommended)

1.  With the server running, open your web browser and navigate to:
    [**http://127.0.0.1:8000/docs**](http://127.0.0.1:8000/docs)

2.  Expand the `POST /price-car` endpoint section.

3.  Click the **"Try it out"** button.

4.  Paste the following JSON into the **Request body** field:
    ```json
    {
      "title": "For Sale: 2007 Honda Accord - runs great!",
      "description": "Selling my reliable Honda Accord sedan. It's a 2007 model with a clean interior, working AC, and 120k miles. No accidents."
    }
    ```

5.  Click the **"Execute"** button to send the request.

### Option B: Using cURL

You can also send a request from your terminal:

```sh
curl -X 'POST' \\
  'http://127.0.0.1:8000/price-car' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: application/json' \\
  -d '{
  "title": "2007 Honda Accord - great condition, runs smooth!",
  "description": "Selling my reliable Honda Accord. 2007 model, clean interior, AC works, 120k miles. No accidents."
}'
```

### Example Successful Response

You should receive a `200 OK` response with a JSON body similar to this:

```json
{
  "make": "Honda",
  "model": "Accord",
  "price": 4750
}
```
---

## Deployment

This API is deployed and live on **Render**.

**Live API Endpoint:** `https://price-my-car-api.onrender.com/price-car`
**Live Interactive Docs:** `https://price-my-car-api.onrender.com/docs`

The deployment was configured with the following settings on Render's free tier:

-   **Build Command**: `pip install -r requirements.txt`
-   **Start Command**:
    ```sh
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    ```
-   **Environment Variables**: The `OPENAI_API_KEY` was set securely in the Render environment settings.

---

## Design Choices

-   **FastAPI**: Chosen for its high performance, native asynchronous support (critical for waiting on LLM API calls without blocking), and automatic data validation and API documentation.
-   **LangChain with `JsonOutputParser`**: Instead of simple string parsing, LangChain's `JsonOutputParser` was used to force the LLM to return a structured, validated JSON object. This drastically increases the reliability of the extraction process.
-   **Asynchronous API Endpoint**: The `/price-car` endpoint is defined with `async def`, allowing it to call the LLM (`await chain.ainvoke(...)`) without blocking the server, enabling it to handle other requests concurrently.
-   **Security**: The OpenAI API key is loaded securely from an environment variable and is never hard-coded into the application, following industry best practices.
