from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
# router.register('flash', views.FlashIndex, basename='flashsale')
router.register('flashsale', views.FlashIdIndex, basename='flashsale')

urlpatterns = [
    path('flash/', views.FlashIndex.as_view(), name="flashsale")
] + router.urls
