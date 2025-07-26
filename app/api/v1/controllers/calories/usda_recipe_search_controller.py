from fastapi import Request
from app.api.deps import BaseController
from app.services.external_services.calorie_service import CalorieService
from app.config.settings import Settings
from app.utils.exceptions import BadRequestException
from app.utils.fuzzy_matcher import fuzzy_compare

settings = Settings()

class UsdaRecipeSearchController(BaseController):
    async def process_get(self, request: Request):
        query = request.query_params.get("query")
        servings = request.query_params.get("servings", 1)
        try:
            servings = float(servings)
            if servings <= 0:
                raise BadRequestException("Servings must be a positive number.")
        except ValueError:
            raise BadRequestException("Servings must be a number.")

        if not query:
            raise BadRequestException("Query parameter is required.")
        service = CalorieService(api_key=settings.USDA_API_KEY)
        response = await service.async_search_food(query)
        # If response is an httpx.Response, get .json()
        if hasattr(response, "json") and callable(response.json):
            data = await response.json() if hasattr(response, "_content_consumed") else response.json()
        else:
            data = response
        if total_hits := data.get("totalHits", 0) == 0:
            return {"message": "No results found for the given query."}
        foods = data.get("foods", [])
        best_match = CalorieService.get_best_fuzzy_match(query, foods)
        calories = None
        calorie_unit = None
        carbs = None
        fat = None
        protein = None
        if best_match:
            for nutrient in best_match.get('foodNutrients', []):
                nutrient_name = nutrient.get('nutrientName', '')
                nutrient_number = nutrient.get('nutrientNumber')

                # Using fuzzy matching for nutrient names and ensuring we only take the first match
                if calories is None and (fuzzy_compare(nutrient_name, 'Energy')['is_fuzzy_match'] or nutrient_number == '208'):
                    calories = nutrient.get('value')
                    calorie_unit = nutrient.get('unitName')
                elif carbs is None and (fuzzy_compare(nutrient_name, 'Carbohydrate, by difference')['is_fuzzy_match'] or nutrient_number == '205'):
                    carbs = nutrient.get('value')
                elif fat is None and (fuzzy_compare(nutrient_name, 'Total lipid (fat)')['is_fuzzy_match'] or nutrient_number == '204'):
                    fat = nutrient.get('value')
                elif protein is None and (fuzzy_compare(nutrient_name, 'Protein')['is_fuzzy_match'] or nutrient_number == '203'):
                    protein = nutrient.get('value')
        return {
            "best_match": {
                "description": best_match.get("description"),
                "food_id": best_match.get("fdcId"),
                "data_type": best_match.get("dataType"),
                "brand_owner": best_match.get("brandOwner"),
                "food_category": best_match.get("foodCategory"),
            },
            "calories": calories,
            "calorie_unit": calorie_unit,
            "carbohydrates_g": carbs,
            "fat_g": fat,
            "protein_g": protein
        }