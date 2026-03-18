from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('position/', views.position, name='position'),
    path('transaction/', views.transaction, name='transaction'),
    path('asset-detail/', views.asset_detail, name='asset_detail'),
    path('api/account-chart-data/', views.get_account_chart_data, name='get_account_chart_data'),
    path('api/asset-chart-data/', views.get_asset_chart_data, name='get_asset_chart_data'),
    path('api/position-distribution/', views.get_position_distribution, name='get_position_distribution'),
    path('api/refresh-snapshot/', views.refresh_snapshot, name='refresh_snapshot'),
]