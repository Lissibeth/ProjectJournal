# main_page/forms.py

from django import forms
from .models import Student
from django.contrib.auth.models import User
from .models import UserProfile

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'patronymic', 'grade', 'course_completion']
        widgets = {
            'grade': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'course_completion': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")
    role = forms.ChoiceField(choices=UserProfile.USER_ROLES, label="Роль")

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'role']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role=self.cleaned_data['role'])
        return user