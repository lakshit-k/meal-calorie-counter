# Meal Calorie Counter

A FastAPI-based application to search for food items and calculate their calorie and macronutrient content using the USDA FoodData Central API.

## Features

- **Food Search**: Search for food items via the USDA API.
- **Nutrient Information**: Retrieves detailed nutrient information, including calories, protein, fat, and carbohydrates.
- **Fuzzy Matching**: Robustly matches food and nutrient names even with slight variations.
- **Database Ready**: Uses Alembic to manage database schema changes for models like `User` and `Calorie`.
- **Asynchronous**: Built with `async` and `await` for high performance.

## Tech Stack

- **Backend**: Python, FastAPI
- **Database**: SQLAlchemy, SQLite
- **Migrations**: Alembic
- **HTTP Client**: `httpx`
- **Configuration**: Pydantic

## Prerequisites

- Python 3.9+
- An API Key from USDA FoodData Central.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd meal-calorie-counter
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    *(Note: A `requirements.txt` file is recommended. You can create one using `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Now, open the `.env` file and add your USDA API Key:
    ```
    USDA_API_KEY="YOUR_API_KEY_HERE"
    ```

5.  **Run database migrations:**
    This will create the SQLite database file (`meal_calorie_db.sqlite3`) and set up the necessary tables defined in your models.
    ```bash
    alembic upgrade head
    ```

## Running the Application

To start the development server, run the following command from the root directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## API Usage

### Search for a Food Item

-   **Endpoint**: `GET /api/v1/calories/usda-recipe-search`
-   **Description**: Searches for a food item and returns the best match with its nutritional information.
-   **Query Parameters**:
    -   `query` (string, required): The name of the food to search for (e.g., "apple").
    -   `servings` (float, optional, default: 1): The number of servings.
-   **Example Request**:
    ```
    http://127.0.0.1:8000/api/v1/calories/usda-recipe-search?query=cheddar%20cheese&servings=1.5
    ```
-   **Example Response**:
    ```json
    {
        "best_match": {
            "description": "Cheese, cheddar",
            "food_id": 171279,
            "data_type": "SR Legacy",
            "brand_owner": null,
            "food_category": "Dairy and Egg Products"
        },
        "calories": 404,
        "calorie_unit": "KCAL",
        "carbohydrates_g": 3.09,
        "fat_g": 33.3,
        "protein_g": 22.9
    }
    ```
