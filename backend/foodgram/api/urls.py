from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from .views import (
#     FavoriteViewSet, FollowListViewSet, FollowViewSet, IngredientViewSet,
#     RecipeViewSet, ShoppingCartViewSet, TagViewSet, UserRetrieve,
# )

app_name = 'api'


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('users/<int:pk>/', UserRetrieve.as_view()),
    # path('', include(v1_router.urls)),
]
