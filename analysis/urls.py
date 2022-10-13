from django.urls import path
from . import views

urlpatterns = [
    path("analysis/", views.Analysis.as_view(), name="analysis"),
    path("recent/", views.RecentlyView.as_view(), name="recently"),
]
