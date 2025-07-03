from django import forms
from .models import Student, Lesson

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['date', 'topic']
