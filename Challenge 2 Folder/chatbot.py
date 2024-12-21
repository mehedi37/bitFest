from fastapi import APIRouter
from transformers import pipeline
from ..database import db

router = APIRouter()

# Load the LLaMA 4 model
chatbot = pipeline('text-generation', model='llama-4')

@router.get("/suggest_recipe/")
async def suggest_recipe(preference: str):
    recipes = await db.recipes.find().to_list(1000)
    recipe_text = "\n".join([f"{recipe['name']}: {recipe['ingredients']}" for recipe in recipes])
    response = chatbot(f"Based on the available recipes, suggest a recipe for someone who wants {preference}. Here are the recipes: {recipe_text}")
    return {"suggestion": response[0]['generated_text']}