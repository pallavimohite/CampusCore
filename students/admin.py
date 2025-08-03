from django.contrib import admin
from .models import Student, Course, Grade


@admin.register(Student)  # Decorator to register Student model with admin
class StudentAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Student model.
    Provides enhanced interface for managing student records.
    """
    # Fields displayed in the admin list view
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'year']
    
    # Filter options in right sidebar for quick filtering
    list_filter = ['year', 'created_at']
    
    # Fields that can be searched using the search box
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    
    # Default ordering of records in admin list view
    ordering = ['student_id']


@admin.register(Course)  # Register Course model with custom admin
class CourseAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Course model.
    Simplified interface for course management.
    """
    # Essential course information displayed in list view
    list_display = ['code', 'name', 'credits']
    
    # Enable search functionality for course code and name
    search_fields = ['code', 'name']


@admin.register(Grade)  # Register Grade model with admin interface
class GradeAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Grade model.
    Manages student-course grade assignments with filtering.
    """
    # Display grade relationships and performance data
    list_display = ['student', 'course', 'grade', 'marks']
    
    # Filter by grade letters for quick grade analysis
    list_filter = ['grade']
