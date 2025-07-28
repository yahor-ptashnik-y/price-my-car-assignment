import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from main import app, get_extraction_chain

client = TestClient(app)


@pytest.fixture
def mocked_llm_chain():
    """
    This fixture creates an AsyncMock for the LLM chain, overrides the
    FastAPI dependency, yields the mock to the test function, and then
    cleans up the override afterwards.
    """
    mock_chain = AsyncMock()

    def fake_get_chain():
        return mock_chain

    app.dependency_overrides[get_extraction_chain] = fake_get_chain

    yield mock_chain

    app.dependency_overrides.clear()


def test_price_car_success(mocked_llm_chain: AsyncMock):
    """
    Tests the "happy path". The fixture handles the setup/teardown.
    """
    request_data = {
        "title": "Selling a 2007 Honda Accord",
        "description": "It's a reliable car."
    }
    mocked_llm_chain.ainvoke.return_value = {"make": "Honda", "model": "Accord"}

    response = client.post("/price-car", json=request_data)

    assert response.status_code == 200
    assert response.json()["make"] == "Honda"
    assert response.json()["model"] == "Accord"
    assert response.json()["price"] > 0


def test_price_car_llm_fails_to_extract(mocked_llm_chain: AsyncMock):
    """
    Tests the case where the LLM can't extract data.
    """
    request_data = {"title": "Looking for a friend", "description": "Must be nice"}
    mocked_llm_chain.ainvoke.return_value = {"make": None, "model": None}

    response = client.post("/price-car", json=request_data)

    assert response.status_code == 422
    assert "Could not extract a valid make and model" in response.json()["detail"]


def test_price_car_pricing_not_found(mocked_llm_chain: AsyncMock):
    """
    Tests the case where the pricing tool doesn't know the car.
    """
    request_data = {"title": "Selling a Tesla", "description": "It's electric!"}
    mocked_llm_chain.ainvoke.return_value = {"make": "Tesla", "model": "Model S"}

    response = client.post("/price-car", json=request_data)

    assert response.status_code == 404
    assert "Pricing for make 'Tesla' and model 'Model S' is not available" in response.json()["detail"]
