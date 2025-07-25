from fastapi import Request
from app.api.deps import BaseController
from app.services.external_services.calorie_service import CalorieService
from app.config.settings import Settings

settings = Settings()

class UsdaRecipeSearchController(BaseController):
    async def process_get(self, request: Request):
        query = request.query_params.get("query")
        if not query:
            return {"error": "Query parameter is required."}
        service = CalorieService(api_key=settings.USDA_API_KEY)
        response = await service.async_search_food(query)
        # If response is an httpx.Response, get .json()
        if hasattr(response, "json") and callable(response.json):
            data = await response.json() if hasattr(response, "_content_consumed") else response.json()
        else:
            data = response
        foods = data.get("foods", [])
        best_match = CalorieService.get_best_fuzzy_match(query, foods)
        calories = None
        calorie_unit = None
        if best_match:
            for nutrient in best_match.get('foodNutrients', []):
                if nutrient.get('nutrientName') == 'Energy' or nutrient.get('nutrientNumber') == '208':
                    calories = nutrient.get('value')
                    calorie_unit = nutrient.get('unitName')
                    break
        return {
            "best_match": best_match,
            "calories": calories,
            "calorie_unit": calorie_unit
        } 