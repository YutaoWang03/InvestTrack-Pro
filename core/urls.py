from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('dashboard'), permanent=False)),
    path('', include('apps.investments.urls')),
    path('', include('apps.risk_engine.urls')),
    path('', include('apps.data_loader.urls')),
]
