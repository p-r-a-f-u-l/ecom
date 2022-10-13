from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
# router.register('product', views.Index, basename='product')
router.register("subbrand", views.SubBrandIndex, basename="subbrand")
router.register("subbranddemo", views.SubbrandIndex, basename="subbrand")
router.register("popular", views.PopularView, basename="popular")
router.register("brand", views.BrandIndex, basename="brand")
# router.register("review", views.ReviewInfo, basename="review")
router.register("toprating", views.TopRating, basename="toprating")
router.register("product", views.Index, basename="index")

urlpatterns = [
    path("brands/", views.CategoryIndex.as_view(), name="brands"),
    path("review/", views.ReviewInfo.as_view(), name="review"),
    path("product/<int:pk>/", views.IndexID.as_view(), name="product_index"),
    path("product/<int:pk>/review/", views.ReviewIndex.as_view(), name="comment"),
    path("", include(router.urls)),
]
