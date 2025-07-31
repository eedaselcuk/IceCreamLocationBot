import os
import requests
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Get top 3 ice cream shops from Google Places API
def get_ice_cream_shops(city_name):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"ice cream shops in {city_name}",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    results = data.get("results", [])
    
    if not results:
        return "No ice cream shops found."

    shops = []
    for place in results[:2]:
        name = place.get("name", "Unknown")
        rating = place.get("rating", "N/A")
        address = place.get("formatted_address", "N/A")
        shops.append(f"{name} - Rating: {rating} - Address: {address}")
    
    return "\n".join(shops)

# Prompt Template
template = """
You are a world-renowned ice cream expert.

The user is currently in {city}, and they love {flavor} ice cream.
Here are some options from Google Maps:

{places}

Based on your expertise, which place would you recommend and why?
"""

prompt = PromptTemplate(
    input_variables=["city", "flavor", "places"],
    template=template
)

# LLM setup
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

# CLI runner
if __name__ == "__main__":
    city = input("Enter a city: ")
    flavor = input("What's your favorite flavor? ")

    print("\n🔍 Fetching top ice cream places...\n")
    places_text = get_ice_cream_shops(city)
    print(places_text)

    print("\n Asking the AI for a recommendation...\n")
    response = chain.invoke({
        "city": city,
        "flavor": flavor,
        "places": places_text
    })

    print("AI's Recommendation: \n")
    print(response)

input("\nPress Enter to exit...")