from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('export/inventory/', views.export_inventory_csv, name='export_inventory'),
    path('export/expired/', views.export_expired_csv, name='export_expired'),
]
