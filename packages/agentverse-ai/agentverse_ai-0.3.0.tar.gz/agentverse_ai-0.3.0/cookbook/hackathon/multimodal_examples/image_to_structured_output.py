from typing import List, Optional

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.openai import OpenAIChat
from pydantic import BaseModel


class Item(BaseModel):
    item_name: str
    price: float


class Invoice(BaseModel):
    restaurant: Optional[str] = None
    address: Optional[str] = None
    bill_number: Optional[str] = None
    items: List[Item]
    total: Optional[float] = None


agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    response_model=Invoice,
)

agent.print_response(
    "Extract the items and prices from the invoice",
    images=[
        Image(
            url="https://upload.wikimedia.org/wikipedia/commons/c/cf/Receipt_California_restaurant_2006.jpg"
        )
    ],
)
