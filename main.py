from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import random
import os
import logging

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

if os.getenv("OPENAI_API_KEY") is None:
    raise SystemExit("Error: OPENAI_API_KEY environment variable not set.")

app = FastAPI(
    title="Price My Car API",
    description="An API to estimate the price of a car using LangChain, OpenAI, and a pricing tool.",
    version="1.0.0"
)

class CarListing(BaseModel):
    title: str
    description: str

class PricedCar(BaseModel):
    make: str
    model: str
    price: int

class ExtractedCarInfo(BaseModel):
    make: str = Field(description="The manufacturer or make of the car, e.g., 'Honda'")
    model: str = Field(description="The specific model of the car, e.g., 'Accord'")


def get_car_price(make: str, model: str) -> int:
    """
    Returns the estimated market price for the given car make and model.
    Raises ValueError if the combination is invalid or unknown.
    """
    known_prices = {
        "honda": { "accord": 4750, "civic": 3500 },
        "toyota": { "camry": 5200, "corolla": 3800 },
        "ford": { "focus": 3200, "mustang": 8500 },
    }
    make_lower = make.lower()
    model_lower = model.lower()

    if make_lower in known_prices and model_lower in known_prices[make_lower]:
        base_price = known_prices[make_lower][model_lower]
        return base_price + random.randint(-250, 250)
    else:
        raise ValueError(f"Pricing for make '{make}' and model '{model}' is not available.")


def create_extraction_chain():
    """
    Creates and returns a LangChain chain for extracting car make and model.
    """
    model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

    parser = JsonOutputParser(pydantic_object=ExtractedCarInfo)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at extracting vehicle information from text. "
                   "You must respond with a JSON object that strictly follows this format: {format_instructions}"),
        ("human", "Extract the make and model from the following car listing:\n"
                  "Title: {title}\nDescription: {description}")
    ]).partial(format_instructions=parser.get_format_instructions())

    chain = (
        prompt | model | parser
    ).with_config(run_name="CarInfoExtraction")
    
    return chain

extraction_chain = create_extraction_chain()


@app.post("/price-car", response_model=PricedCar)
async def price_car_endpoint(listing: CarListing):
    """
    Accepts car listing data, extracts make and model using an LLM,
    gets a price, and returns the result.
    """
    try:
        extracted_info = await extraction_chain.ainvoke({
            "title": listing.title,
            "description": listing.description
        })
    except OutputParserException as e:
        logging.error(f"OutputParserException occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail="The server had trouble understanding the response from the AI model. Please try again."
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred. Please try again later."
        )

    make = extracted_info.get("make")
    model = extracted_info.get("model")

    if not make or not model:
        raise HTTPException(
            status_code=422,
            detail="Could not extract a valid make and model from the provided text. Please provide a more descriptive listing."
        )

    try:
        price = get_car_price(make=make, model=model)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return PricedCar(make=make, model=model, price=price)
