from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Student, Course, Grade
from .forms import StudentForm, CourseForm, GradeForm, UserRegisterForm


# Authentication Views
def register(request):
    """
    Handle user registration with automatic login upon successful registration.
    Creates new user account and redirects to student list.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save new user to database
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            # Automatically log in the newly registered user
            login(request, user)
            return redirect('student_list')
    else:
        # GET request - display empty registration form
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# Dashboard
@login_required  # Ensures only authenticated users can access dashboard
def dashboard(request):
    """
    Display system overview with statistics and recent activity.
    Shows total counts and recently added students.
    """
    # Calculate statistics for dashboard display
    context = {
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        'total_grades': Grade.objects.count(),
        'recent_students': Student.objects.order_by('-created_at')[:5]  # Last 5 students added
    }
    return render(request, 'students/dashboard.html', context)


# STUDENT CRUD OPERATIONS

# CREATE - Add new student
@login_required
def student_create(request):
    """
    Handle both GET and POST requests for creating new students.
    GET: Display empty form, POST: Process form and save to database.
    """
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Save form data to database
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        # GET request - show empty form
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {
        'form': form, 
        'title': 'Add New Student'
    })


# READ - List all students
@login_required
def student_list(request):
    """
    Display paginated list of students with search functionality.
    Implements search across multiple fields and pagination for performance.
    """
    # Start with all students ordered by student ID
    student_list = Student.objects.all().order_by('student_id')
    
    # Search functionality - filter by name or student ID
    search = request.GET.get('search')
    if search:
        # Search across multiple fields using case-insensitive matching
        student_list = student_list.filter(
            first_name__icontains=search
        ) or student_list.filter(
            last_name__icontains=search
        ) or student_list.filter(
            student_id__icontains=search
        )
    
    # Pagination - limit to 10 students per page for better performance
    paginator = Paginator(student_list, 10)  # 10 students per page
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)
    
    return render(request, 'students/student_list.html', {'students': students})


# READ - Student detail view
@login_required
def student_detail(request, pk):
    """
    Display detailed information for a specific student including grades.
    Uses get_object_or_404 for proper error handling.
    """
    # Get student or return 404 if not found
    student = get_object_or_404(Student, pk=pk)
    # Get all grades for this student
    grades = Grade.objects.filter(student=student)
    return render(request, 'students/student_detail.html', {
        'student': student,
        'grades': grades
    })


# UPDATE - Edit student
@login_required
def student_update(request, pk):
    """
    Handle student information updates.
    Pre-populates form with existing data for editing.
    """
    # Get existing student record
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        # Process form submission with existing student instance
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        # GET request - pre-populate form with existing student data
        form = StudentForm(instance=student)
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Edit Student',
        'student': student
    })


# DELETE - Remove student
@login_required
def student_delete(request, pk):
    """
    Handle student deletion with confirmation step.
    Shows confirmation page before actual deletion for safety.
    """
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        # User confirmed deletion - proceed with removal
        student.delete()  # This also deletes related grades due to CASCADE
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    
    # GET request - show confirmation page
    return render(request, 'students/student_confirm_delete.html', {'student': student})


# COURSE OPERATIONS
@login_required
def course_list(request):
    """
    Display list of all available courses.
    Simple view showing all courses without pagination.
    """
    courses = Course.objects.all()  # Get all courses
    return render(request, 'students/course_list.html', {'courses': courses})


@login_required
def course_create(request):
    """
    Handle course creation with form validation.
    Creates new courses and redirects to course list upon success.
    """
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # Save new course to database
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('course_list')
    else:
        # GET request - display empty course form
        form = CourseForm()
    
    return render(request, 'students/course_form.html', {'form': form})


# GRADE OPERATIONS
@login_required
def grade_create(request):
    """
    Handle grade assignment linking students to courses with performance data.
    Creates grade records for student-course combinations.
    """
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            # Save grade record to database
            form.save()
            messages.success(request, 'Grade added successfully!')
            return redirect('student_list')  # Redirect to student list to view results
    else:
        # GET request - show empty grade form
        form = GradeForm()
    
    return render(request, 'students/grade_form.html', {'form': form})
