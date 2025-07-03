from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    date = models.DateField()
    topic = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.date} — {self.topic}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.name} — {self.lesson.date}: {'Присутствовал' if self.present else 'Отсутствовал'}"
