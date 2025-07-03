from django.urls import path
from . import views

urlpatterns = [
    # Студенты
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),

    # Уроки
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/add/', views.lesson_add, name='lesson_add'),

    # Посещаемость
    path('lessons/<int:lesson_id>/attendance/', views.attendance_list, name='attendance_list'),
    path('lessons/<int:lesson_id>/attendance/export_excel/', views.export_attendance_excel, name='export_attendance_excel'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student_delete'),
    path('lessons/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'),

]
