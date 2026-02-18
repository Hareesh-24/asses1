from django.urls import path
from . import views

urlpatterns = [
    path('api/recipes', views.recipe_list_api, name='recipe-list'),
    path('api/recipes/search', views.recipe_search_api, name='recipe-search'),
]