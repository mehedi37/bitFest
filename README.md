# Recipe Management API
A FastAPI-based API for managing recipes and ingredients with image processing capabilities.

## ⚙️Setup
- install requirements: `pip install -r requirements.txt`
- configure environment variables in `.env` file
  > MONGODB_URI="your_mongodb_connection_string"
  > DATABASE_NAME="your_database_name"
- run the app: `uvicorn main:app --reload`

## API Documentation
Ingredients Management

### Add Ingredient
- Route: `/ingredients`
- Method: `POST`
- Request Body:
  ```json
  {
    "name": "ingredient_name",
    "category": "ingredient_category"
  }
  ```
- Response:
  ```json
  {
    "id": "ingredient_id",
    "name": "ingredient_name",
    "category": "ingredient_category"
  }
  ```

### Update Ingredient
- Route: `/ingredients/{ingredient_id}`
- Method: `PUT`
- Request Body:
  ```json
  {
    "name": "ingredient_name",
    "category": "ingredient_category"
  }
  ```

### List Ingredients
- Route: `/ingredients/`
- Method: `GET`
- Response:
  ```json
  [
    {
        "name": "Tomato",
        "quantity": 2.5,
        "unit": "cups",
        "last_updated": "2024-01-20T10:30:00Z"
    }
  ]
  ```

### Delete Ingredient
- Route: `/ingredients/{ingredient_id}`
- Method: `DELETE`

## Recipe Management

### Add Recipe
- Route: `/recipes/text/`
- Method: `POST`
- Payload:
  ```json
  {
    "name": "Spaghetti Bolognese",
    "ingredients": ["Spaghetti", "Ground Beef", "Tomato Sauce"],
    "instructions": "Boil spaghetti. Cook beef. Mix with sauce."
  }
  ```

### Add Recipe (Image)
- Route: `/recipes/image`
- Method: `POST`
- Form Data:
  - `image`: image file
  - `name`: recipe name
  - `ingredients`: comma-separated list of ingredients
  - `instructions`: recipe instructions

### Get All Recipes
- Route: `/recipes/`
- Method: `GET`
- Response:
  ```json
  [
    {
        "name": "Spaghetti Bolognese",
        "ingredients": ["Spaghetti", "Ground Beef", "Tomato Sauce"],
        "instructions": "Boil spaghetti. Cook beef. Mix with sauce.",
        "image_url": "/images/spaghetti.jpg",
        "created_at": "2024-01-20T10:30:00Z"
    }
  ]
  ```

### Get Recipe by ID

- Route: `/recipes/{recipe_id}`
- Method: `GET`
- Response:
  ```json
  {
    "name": "Spaghetti Bolognese",
    "ingredients": ["Spaghetti", "Ground Beef", "Tomato Sauce"],
    "instructions": "Boil spaghetti. Cook beef. Mix with sauce.",
    "image_url": "/images/spaghetti.jpg",
    "created_at": "2024-01-20T10:30:00Z"
  }
  ```

## OCR Features
### Upload Recipe Image
- Route: `/upload_recipe_image/`
- Method: `POST`
- Form Data:
  - `file`: image file
- Response:
  ```json
  {
    "message": "Recipe added successfully from image"
  }
  ```

## Chatbot Integration
### Get Recipe Suggestion

- Route: `/suggest_recipe/`
- Method: `POST`
- Query Parameters:
  - `preference`: user message
- Response:
  ```json
  {
    "suggestion": "Based on your preference, I recommend..."
  }
  ```

## Features
- MongoDB integration for data persistence
- Image processing with OCR capabilities
- Recipe suggestions using LLaMA 4 model
- File-based recipe backup
- Image upload support
- RESTful API design

## Dependencies
- FastAPI
- MongoDB
- PyTesseract
- Pillow
- Transformers
- Python-dotenv