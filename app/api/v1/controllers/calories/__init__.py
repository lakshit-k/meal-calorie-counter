from .usda_recipe_search_controller import UsdaRecipeSearchController

routes = [
    UsdaRecipeSearchController("/calories/usda-recipe-search").router
]
