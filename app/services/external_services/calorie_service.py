from app.services.base_service import BaseService
from app.utils.constant import CALORIE_API
from app.utils.fuzzy_matcher import fuzzy_compare

class CalorieService(BaseService):
    def __init__(self, api_key: str):
        super().__init__(base_url=CALORIE_API)
        self.api_key = api_key

    def search_food(self, query: str, page_size: int = 100):
        self.set_endpoint("foods/search")
        self.set_method("GET")
        self.set_params({
            "api_key": self.api_key,
            "query": query,
            # "dataType": data_type,
            "pageSize": page_size
        })
        return self.invoke()

    async def async_search_food(self, query: str, page_size: int = 100):
        self.set_endpoint("foods/search")
        self.set_method("GET")
        self.set_params({
            "api_key": self.api_key,
            "query": query,
            # "dataType": data_type,
            "pageSize": page_size
        })
        return await self.async_invoke()

    @staticmethod
    def get_best_fuzzy_match(query: str, foods: list) -> dict:
        """
        Compare the search query with each food's description using fuzzy_compare.
        Return the food with the highest similarity ratio and the ratio score.
        """
        best_food = None
        best_score = -1
        for food in foods:
            desc = food.get('description', '')
            result = fuzzy_compare(query, desc)
            if result['ratio'] > best_score:
                best_score = result['ratio']
                best_food = food.copy()
                best_food['fuzzy_score'] = best_score
            
            if result["is_fuzzy_match"]:
                break
            
        return best_food if best_food else {} 