from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('address', views.AddressIndex, basename='address')
router.register('card', views.CardIndex, basename='card')
# router.register('fav', views.FavItemIndex, basename='fav')
router.register('addfav', views.AddFaveItemIndex, basename='addfav')
router.register('cart', views.CartIndex, basename='cart')
router.register('addcart', views.AddCartItemIndex, basename='addcart')
router.register('payment', views.PaymentIndex, basename='payment')
router.register('mastercart', views.MasterCartIndex, basename='mastercart')
# router.register('payment_get', views.PaymentIndexSe, basename='payemt_get')

urlpatterns = [
    path('fav/', views.FavItemIndex.as_view(), name="fav"),
    path('payment_get/', views.PaymentIndexSe.as_view(), name="payement_get"),
    path('payment_get/<pk>/', views.PaymentIndexID.as_view(), name="payement_get"),
    path('', include(router.urls)),
]
