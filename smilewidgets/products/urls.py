from django.urls import path

from .views import GetPriceView

urlpatterns = [path("api/get-price", GetPriceView.as_view(), name="get-price")]
