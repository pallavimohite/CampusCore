from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Authentication
    path('register/', views.register, name='register'),
    
    # Student CRUD
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_add'),
    
    # Grade URLs
    path('grades/add/', views.grade_create, name='grade_add'),
]
