from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet
)

app_name = 'api'


v1_router = DefaultRouter()
v1_router.register(r'tags', TagViewSet)
v1_router.register(r'ingredients', IngredientViewSet)
v1_router.register(r'recipes', RecipeViewSet)
v1_router.register(r'users', UserViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(v1_router.urls)),
]
