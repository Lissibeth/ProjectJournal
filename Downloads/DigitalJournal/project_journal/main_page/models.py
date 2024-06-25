from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    grade = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    course_completion = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not (1 <= self.grade <= 5):
            raise ValidationError("Grade must be between 1 and 5.")
        if not (0 <= self.course_completion <= 100):
            raise ValidationError("Course completion must be between 0 и 100.")

class UserProfile(models.Model):
    USER_ROLES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=7, choices=USER_ROLES)

    def __str__(self):
        return self.user.username
