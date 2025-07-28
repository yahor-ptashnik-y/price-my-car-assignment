# Price My Car API - Candidate Assignment

This project is an implementation of the "Price My Car" API assignment. It is a REST API built with FastAPI that takes a car's title and description, uses a Large Language Model (LLM) via LangChain to extract its make and model, and returns an estimated price.

You can run this project by following the [local setup instructions](#getting-started-local-setup) or test the [live deployed version](#deployment) directly.

---

## Features

-   **Intelligent Extraction**: Uses **OpenAI's GPT model** via **LangChain** to reliably extract structured `make` and `model` data from unstructured text.
-   **REST API Endpoint**: A `POST /price-car` endpoint that accepts car listing details.
-   **Pricing Tool Integration**: Connects to a simulated Python tool (`get_car_price`) to retrieve a price estimate.
-   **Robust Error Handling**: Gracefully handles potential errors, such as LLM extraction failures or unknown vehicle models, returning clear error messages with appropriate HTTP status codes.
-   **Production-Ready Logging**: Logs detailed exceptions on the server for debugging while presenting generic, user-friendly error messages via the API to maintain security.
-   **Comprehensive Testing**: Includes a test suite using `pytest` that verifies success cases and edge-case failures. It leverages FastAPI's **Dependency Injection** system to mock the external LLM service, ensuring tests are fast, reliable, and isolated.
-   **Automated Code Formatting**: Uses **Black** and **`pre-commit`** to automatically enforce a consistent, PEP 8-compliant code style, guaranteeing code quality and readability.
-   **Secure & Asynchronous**: Follows best practices by using environment variables for API keys and leveraging asynchronous processing for high performance.

---

## Tech Stack

-   **Framework**: FastAPI
-   **LLM Framework**: LangChain
-   **LLM Provider**: OpenAI
-   **Production Server**: Gunicorn
-   **Development Server**: Uvicorn
-   **Testing**: Pytest, unittest.mock
-   **Code Formatting**: Black, pre-commit
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

**Step 5: Set up the pre-commit hook**

This project uses `pre-commit` to automatically format code before each commit. Before that, you have to install packages used only for develepoment purposes.

```sh
pip install -r requirements-dev.txt
```

This is a one-time setup command.

```sh
pre-commit install
```

---

## Running the Application Locally

For local development, start the API server with Uvicorn.

```sh
uvicorn main:app
```

The server will start and listen on `http://127.0.0.1:8000`. Detailed error logs will be printed to the console.

Add `--reload` flag that enables hot-reloading, which automatically restarts the server when you make changes to the code.

```sh
uvicorn main:app --reload
```

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

## Code Quality and Formatting

This project uses the **Black** code formatter to ensure a consistent, PEP 8-compliant style. The line length is configured to a maximum of 79 characters via the `pyproject.toml` file.

To maintain code quality automatically, a **`pre-commit` hook** is configured. This hook runs Black on all staged files before a commit is created. If formatting changes are made, the commit will be aborted, allowing you to review and re-stage the formatted files. This guarantees that every commit adheres to the project's style guide.

---

## Running Tests

This project includes a test suite to ensure reliability. The tests mock the external OpenAI API call to ensure they are fast and do not require an active internet connection or API key.

To run the tests, execute the following command from the project root:

```sh
pytest --verbose
```

---

## Deployment

This API is deployed and live on **Render**.

> **Note on Free Tier Hosting**
> This project is hosted on Render's free tier, which automatically spins down the service after a period of inactivity. As a result, the first request may take **30-60 seconds** to process as the server wakes up.
>
> If you see an error message or the page doesn't load immediately, please **wait a moment and then refresh your browser**. The application will be available once the cold start is complete.

**Live API Endpoint:** https://price-my-car-api.onrender.com/price-car

**Live Interactive Docs:** https://price-my-car-api.onrender.com/docs

The deployment was configured with the following settings:
-   **Build Command**: `pip install -r requirements.txt`
-   **Start Command**:
    ```sh
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    ```
-   **Environment Variables**: The `OPENAI_API_KEY` was set securely in the Render environment settings.

---

## Design Choices

-   **FastAPI with Dependency Injection**: The application uses FastAPI's native **Dependency Injection** system (`Depends`) to provide the LLM chain to the API endpoint. This decouples the endpoint from the global state, making the code more modular. Crucially, it allows for robust and reliable testing by using `app.dependency_overrides` to inject a mock object during tests.
-   **LangChain with `JsonOutputParser`**: To ensure the LLM returns predictable, structured data, LangChain's `JsonOutputParser` was used. This forces the model's output into a validated JSON object, drastically increasing the reliability of the extraction process.
-   **Asynchronous Endpoint**: The `/price-car` endpoint is defined with `async def`, allowing it to call the LLM (`await chain.ainvoke(...)`) without blocking the server. This is critical for performance, enabling the server to handle other requests concurrently while waiting for the network response from OpenAI.
-   **Secure Error Handling & Logging**: The application distinguishes between client errors (4xx) and server errors (5xx). For server-side errors, detailed exceptions are logged for developer debugging, but only a generic "Internal Server Error" message is sent to the user. This prevents leaking potentially sensitive information about the application's internal workings.
-   **Secure API Keys**: The OpenAI API key is loaded securely from an environment variable and is never hard-coded into the application.
