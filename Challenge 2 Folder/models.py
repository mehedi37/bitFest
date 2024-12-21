# models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Ingredient(BaseModel):
    name: str = Field(..., example="Tomato")
    quantity: float = Field(..., example=2.5)
    unit: str = Field(..., example="cups")
    last_updated: Optional[datetime] = Field(default_factory=datetime.utcnow)

class UpdateIngredient(BaseModel):
    quantity: Optional[float] = Field(None, example=3.0)
    unit: Optional[str] = Field(None, example="liters")
    name: Optional[str] = Field(None, example="Tomato")

class Recipe(BaseModel):
    name: str = Field(..., example="Spaghetti Bolognese")
    ingredients: List[str] = Field(..., example=["Spaghetti", "Ground Beef", "Tomato Sauce"])
    instructions: str = Field(..., example="Boil spaghetti. Cook beef. Mix with sauce.")
    image_url: Optional[str] = Field(None, example="http://example.com/image.jpg")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
