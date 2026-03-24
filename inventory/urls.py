from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'), # Default to dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard_alias'),
    path('staff/dashboard/', views.DashboardView.as_view(), name='staff_dashboard'), # Explicit
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('medicines/add/', views.MedicineCreateView.as_view(), name='medicine_add'),
    path('medicines/<int:pk>/edit/', views.MedicineUpdateView.as_view(), name='medicine_edit'),
    path('medicines/<int:pk>/delete/', views.MedicineDeleteView.as_view(), name='medicine_delete'),
    path('alerts/<int:pk>/resolve/', views.resolve_alert, name='alert_resolve'),
]
