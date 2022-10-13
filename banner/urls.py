from . import views
from django.urls import path

urlpatterns = [
    path('banner/', views.BannerIndex.as_view(), name='banner'),
]
