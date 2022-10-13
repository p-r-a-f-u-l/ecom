from . import views
from django.urls import path

urlpatterns = [
    path('forgot_password/', views.forgetpassword, name="email-forget"),
    path('logout/', views.Logout.as_view(), name="logout"),
]
