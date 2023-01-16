from django.urls import path

from . import views

urlpatterns = [
    path('', views.bitcoin_price_view, name='bitcoin_price_view'),
    path('', views.search_view, name='search_view'),
    
]