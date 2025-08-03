from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Course, Grade


class StudentForm(forms.ModelForm):
    """
    ModelForm for Student model with custom widgets and validation.
    Automatically generates form fields from model fields.
    """
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'year', 'courses']
        
        # Custom widgets for Bootstrap styling and better user experience
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'STU001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'courses': forms.CheckboxSelectMultiple(),  # Allow multiple course selection
        }


class CourseForm(forms.ModelForm):
    """
    ModelForm for Course model with Bootstrap styling.
    Handles course creation and updates.
    """
    class Meta:
        model = Course
        fields = ['name', 'code', 'credits']
        
        # Bootstrap styling for consistent UI appearance
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
        }


class GradeForm(forms.ModelForm):
    """
    ModelForm for Grade model handling student-course grade assignments.
    Links students to courses with their academic performance.
    """
    class Meta:
        model = Grade
        fields = ['student', 'course', 'grade', 'marks']
        
        # Form widgets with validation constraints
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }


class UserRegisterForm(UserCreationForm):
    """
    Extended user registration form with email field.
    Inherits from Django's built-in UserCreationForm for security.
    """
    # Additional email field for user registration
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        """Apply Bootstrap styling to all form fields."""
        super().__init__(*args, **kwargs)
        # Loop through all fields and add Bootstrap classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
