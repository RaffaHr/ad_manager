from django.urls import path
from . import views

urlpatterns = [
    path('get_list_sku_ids', views.get_list_sku_ids, name="get_list_sku_ids" ),
]
