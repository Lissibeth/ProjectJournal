# main_page/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Student
from .forms import UserRegistrationForm
from collections import defaultdict, Counter
from .forms import StudentForm
from django.db.models import Avg
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect
from .models import Student, UserProfile
from .models import Note
from .forms import NoteForm

@login_required
def profile_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    context = {'user_profile': user_profile}

    if user_profile.role == 'student':
        student = get_object_or_404(Student, user=request.user)
        context['student'] = student

    return render(request, 'main_page/profile.html', context)

# Определяем функцию is_teacher
def is_teacher(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'teacher'



def home(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    return render(request, 'main_page/home.html', context)

@login_required
def diagrams(request):
    students = Student.objects.all()
    grouped_students = defaultdict(list)
    
    # Группируем студентов по проценту выполнения курса
    for student in students:
        grouped_students[student.course_completion].append(student)
    
    # Подготавливаем данные для передачи в шаблон
    grouped_data = [
        {
            'students': students,
            'count': len(students),
            'completion_percentage': completion_percentage
        }
        for completion_percentage, students in grouped_students.items()
    ]
    
    # Находим проценты выполнения, которые имеют наибольшее количество студентов
    completion_counts = Counter(student.course_completion for student in students)
    max_count = max(completion_counts.values())
    most_common_completions = [completion for completion, count in completion_counts.items() if count == max_count]

    return render(request, 'main_page/diagrams.html', {
        'grouped_students': grouped_data,
        'most_common_completions': most_common_completions
    })


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'main_page/signup.html', {'form': form})

@login_required
def students(request):
    students = Student.objects.all()
    return render(request, 'main_page/students.html', {'students': students})

@csrf_protect
@user_passes_test(is_teacher)
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm()
    return render(request, 'main_page/add_student.html', {'form': form})

@csrf_protect
@user_passes_test(is_teacher)
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('students')

@csrf_protect
@user_passes_test(is_teacher)
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm(instance=student)
    return render(request, 'main_page/edit_student.html', {'form': form})

@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'main_page/notes_list.html', {'notes': notes})

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('notes_list')
    else:
        form = NoteForm()
    return render(request, 'main_page/add_note.html', {'form': form})

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'main_page/edit_note.html', {'form': form})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')
    return render(request, 'main_page/delete_note.html', {'note': note})