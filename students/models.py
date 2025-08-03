from django.db import models
from django.urls import reverse


class Course(models.Model):
    """
    Course model to store academic course information.
    Each course can have multiple students enrolled through Many-to-Many relationship.
    """
    name = models.CharField(max_length=100)  # Full course name (e.g., Computer Science)
    code = models.CharField(max_length=10, unique=True)  # Unique course identifier (e.g., CS101)
    credits = models.IntegerField(default=3)  # Credit hours for this course
    
    def __str__(self):
        # Display format: "CS101 - Computer Science" for dropdowns and admin
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['name']  # Sort courses alphabetically for better user experience


class Student(models.Model):
    """
    Student model storing personal and academic information.
    Django automatically creates 'id' field as Primary Key (AutoField).
    """
    # Django automatically creates 'id' as Primary Key
    
    # Academic year choices - constrains input to valid academic levels
    YEAR_CHOICES = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=50)  # Student's first name
    last_name = models.CharField(max_length=50)   # Student's last name
    email = models.EmailField(unique=True)        # Unique email for login and communication
    student_id = models.CharField(max_length=20, unique=True)  # Unique student identifier
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)  # Current academic year
    
    # Relationships
    # Many-to-Many: One student can enroll in multiple courses
    courses = models.ManyToManyField(Course, blank=True)
    
    # Timestamps - automatically managed by Django for audit trail
    created_at = models.DateTimeField(auto_now_add=True)  # Set once on creation
    updated_at = models.DateTimeField(auto_now=True)      # Updated on every save
    
    def __str__(self):
        # String representation for admin interface and debugging
        return f"{self.student_id} - {self.first_name} {self.last_name}"
    
    def get_full_name(self):
        """Return formatted full name for display purposes."""
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        """Return canonical URL for this student's detail page."""
        return reverse('student_detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['student_id']  # Default ordering by student ID


class Grade(models.Model):
    """
    Grade model creating relationship between Students and Courses with performance data.
    Implements one grade per student per course business rule.
    """
    # Foreign Key relationships with CASCADE delete for data integrity
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Student who received grade
    course = models.ForeignKey(Course, on_delete=models.CASCADE)    # Course for which grade was given
    
    # Letter grade choices with score ranges for clarity
    GRADE_CHOICES = [
        ('A', 'A (90-100)'),
        ('B', 'B (80-89)'),
        ('C', 'C (70-79)'),
        ('D', 'D (60-69)'),
        ('F', 'F (Below 60)'),
    ]
    
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)  # Letter grade assigned
    marks = models.IntegerField()  # Numerical marks out of 100
    
    def __str__(self):
        # Display format for admin and debugging
        return f"{self.student.get_full_name()} - {self.course.name} - {self.grade}"
    
    class Meta:
        # Business rule: One grade per student per course to prevent duplicates
        unique_together = ['student', 'course']
