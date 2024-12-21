from fastapi import APIRouter, UploadFile, File, HTTPException
from ..database import db
import pytesseract
from PIL import Image
import io

router = APIRouter()

@router.post("/upload_recipe_image/")
async def upload_recipe_image(file: UploadFile = File(...)):
    try:
        image = Image.open(io.BytesIO(await file.read()))
        text = pytesseract.image_to_string(image)
        # Assuming the text format is similar to the text file parsing
        name, ingredients, taste, reviews, cuisine_type, preparation_time = text.strip().split(',')
        recipe = {
            "name": name,
            "ingredients": ingredients,
            "taste": taste,
            "reviews": reviews,
            "cuisine_type": cuisine_type,
            "preparation_time": preparation_time
        }
        await db.recipes.insert_one(recipe)
        return {"message": "Recipe added successfully from image"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))