from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Lesson, Attendance
from .forms import StudentForm, LessonForm
from openpyxl import Workbook
from django.http import HttpResponse

# --- Студенты ---

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})

def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'attendance/student_form.html', {'form': form})

# --- Уроки ---

def lesson_list(request):
    lessons = Lesson.objects.order_by('-date')
    return render(request, 'attendance/lesson_list.html', {'lessons': lessons})

def lesson_add(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lesson_list')
    else:
        form = LessonForm()
    return render(request, 'attendance/lesson_form.html', {'form': form})

# --- Посещаемость ---

def attendance_list(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    students = Student.objects.all()

    for student in students:
        Attendance.objects.get_or_create(student=student, lesson=lesson)

    attendances = Attendance.objects.filter(lesson=lesson).select_related('student')

    if request.method == 'POST':
        for att in attendances:
            present_value = request.POST.get(f'present_{att.student.id}') == 'on'
            if att.present != present_value:
                att.present = present_value
                att.save()
        return redirect('attendance_list', lesson_id=lesson.id)

    return render(request, 'attendance/attendance_list.html', {
        'lesson': lesson,
        'attendances': attendances,
    })

# --- Экспорт в Excel ---

def export_attendance_excel(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    attendances = Attendance.objects.filter(lesson=lesson).select_related('student')

    wb = Workbook()
    ws = wb.active
    ws.title = "Посещаемость"

    ws.append(['Студент', 'Дата урока', 'Тема урока', 'Присутствие'])
    for att in attendances:
        ws.append([
            att.student.name,
            lesson.date.strftime('%Y-%m-%d'),
            lesson.topic,
            'Да' if att.present else 'Нет'
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename=attendance_{lesson.date}.xlsx'
    wb.save(response)
    return response
from django.shortcuts import render, redirect, get_object_or_404

def student_delete(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'attendance/student_confirm_delete.html', {'student': student})
from django.shortcuts import get_object_or_404, redirect

def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.method == 'POST':
        lesson.delete()
        return redirect('lesson_list')
    return render(request, 'attendance/lesson_confirm_delete.html', {'lesson': lesson})
