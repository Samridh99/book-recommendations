from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RecommendationViewSet, LikeViewSet, IndexView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/', include(router.urls)),
]