from django.urls import path
from . import views

urlpatterns = [
    path("", views.APIRootView.as_view(), name="api-root"),
    path("crops/", views.CropList.as_view(), name="crop-list"),
    path("crops/<int:pk>", views.CropDetail.as_view(), name="crop-detail"),
    path("seasons/", views.SeasonList.as_view(), name="season-list"),
    path("quality-chance/", views.QualityList.as_view(), name="quality-list"),
    path("gold-per-day/", views.GoldPerDayList.as_view(), name="gold-per-day")
]