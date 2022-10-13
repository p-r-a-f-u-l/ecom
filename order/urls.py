from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("order", views.OrderIDIndex, basename='order')

urlpatterns = [
    path('order/', views.OrderIndex.as_view(), name='order'),
    # path('order/<int:pk>/', views.OrderIDIndex.as_view(), name='order'),
    path('orderinfo/',
         views.OrderInfoInex.as_view(), name='orderinfo'),
    path('checkpincode/', views.CheckPinCode.as_view(), name="checkpin")
] + router.urls
