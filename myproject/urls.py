from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # если не используешь админку — можно убрать
    path('', include('attendance.urls')),  # подключаем маршруты приложения attendance
]
