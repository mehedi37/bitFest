# main.py
import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
from models import Ingredient, UpdateIngredient, Recipe
from database import ingredients_collection, recipes_collection
from datetime import datetime
from bson.objectid import ObjectId
import pytesseract
from PIL import Image
import shutil

app = FastAPI(title="Cookbook Management API")

# Ensure recipes.txt exists
if not os.path.exists("recipes.txt"):
    with open("recipes.txt", "w") as f:
        f.write("My Favorite Recipes\n===================\n\n")


# Helper function to write to recipes.txt
def append_recipe_to_file(recipe: Recipe):
    with open("recipes.txt", "a") as f:
        f.write(f"Name: {recipe.name}\n")
        f.write("Ingredients:\n")
        for ingredient in recipe.ingredients:
            f.write(f" - {ingredient}\n")
        f.write(f"Instructions: {recipe.instructions}\n")
        if recipe.image_url:
            f.write(f"Image URL: {recipe.image_url}\n")
        f.write(f"Created At: {recipe.created_at}\n")
        f.write("\n-------------------\n\n")


# Endpoint to add a new ingredient
@app.post("/ingredients/", response_model=Ingredient)
def add_ingredient(ingredient: Ingredient):
    # Check if ingredient already exists
    existing = ingredients_collection.find_one({"name": ingredient.name})
    if existing:
        raise HTTPException(status_code=400, detail="Ingredient already exists.")
    ingredient.last_updated = datetime.utcnow()
    result = ingredients_collection.insert_one(ingredient.dict())
    ingredient._id = str(result.inserted_id)
    return ingredient


# Endpoint to update an existing ingredient
@app.put("/ingredients/{ingredient_id}", response_model=Ingredient)
def update_ingredient(ingredient_id: str, ingredient: UpdateIngredient):
    update_data = ingredient.dict(exclude_unset=True)
    if update_data:
        update_data["last_updated"] = datetime.utcnow()
        result = ingredients_collection.update_one({"_id": ObjectId(ingredient_id)}, {"$set": update_data})
        if result.matched_count:
            updated_ingredient = ingredients_collection.find_one({"_id": ObjectId(ingredient_id)})
            return Ingredient(**updated_ingredient)
    raise HTTPException(status_code=404, detail="Ingredient not found.")


# Endpoint to list all ingredients
@app.get("/ingredients/", response_model=List[Ingredient])
def list_ingredients():
    ingredients = list(ingredients_collection.find())
    return [Ingredient(**ingredient) for ingredient in ingredients]


# Endpoint to delete an ingredient
@app.delete("/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: str):
    result = ingredients_collection.delete_one({"_id": ObjectId(ingredient_id)})
    if result.deleted_count:
        return JSONResponse(content={"message": "Ingredient deleted successfully."})
    raise HTTPException(status_code=404, detail="Ingredient not found.")


# Endpoint to add a new recipe via text
@app.post("/recipes/text/", response_model=Recipe)
def add_recipe_text(recipe: Recipe):
    # Check if recipe already exists
    existing = recipes_collection.find_one({"name": recipe.name})
    if existing:
        raise HTTPException(status_code=400, detail="Recipe already exists.")
    recipe.created_at = datetime.utcnow()
    result = recipes_collection.insert_one(recipe.dict())
    recipe._id = str(result.inserted_id)
    append_recipe_to_file(recipe)
    return recipe


# Endpoint to add a new recipe via image
@app.post("/recipes/image/", response_model=Recipe)
async def add_recipe_image(name: str = Form(...),
                           instructions: str = Form(...),
                           ingredients: List[str] = Form(...),
                           image: UploadFile = File(...)):
    # Save the uploaded image temporarily
    temp_image_path = f"temp_{image.filename}"
    with open(temp_image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    try:
        # Perform OCR to extract text (optional, since instructions are provided)
        extracted_text = pytesseract.image_to_string(Image.open(temp_image_path))
        # Here you can process extracted_text if needed

        # Create Recipe object
        recipe = Recipe(
            name=name,
            ingredients=ingredients,
            instructions=instructions,
            image_url=f"/images/{image.filename}",
            created_at=datetime.utcnow()
        )

        # Save recipe to MongoDB
        result = recipes_collection.insert_one(recipe.dict())
        recipe.id = str(result.inserted_id)

        # Append to recipes.txt
        append_recipe_to_file(recipe)

        # Optionally, move the image to a static directory
        images_dir = "images"
        os.makedirs(images_dir, exist_ok=True)
        shutil.move(temp_image_path, os.path.join(images_dir, image.filename))

        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temp image if it still exists
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)


# Endpoint to retrieve all recipes
@app.get("/recipes/", response_model=List[Recipe])
def get_recipes():
    recipes = list(recipes_collection.find())
    return [Recipe(**recipe) for recipe in recipes]


# Endpoint to retrieve a single recipe by ID
@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: str):
    recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
    if recipe:
        return Recipe(**recipe)
    raise HTTPException(status_code=404, detail="Recipe not found.")
