
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_page.urls')),  # Включаем URL-адреса из приложения main_page
]
