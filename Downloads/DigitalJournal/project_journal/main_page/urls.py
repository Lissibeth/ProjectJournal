# main_page/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('diagrams/', views.diagrams, name='diagrams'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='main_page/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('edit/<int:student_id>/',views.edit_student, name='edit_student'),
    path('students/add/', views.add_student, name='add_student'),
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/add/', views.add_note, name='add_note'),
    path('notes/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
]