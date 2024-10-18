from django.shortcuts import render, redirect
from .models import Student
from django.http import HttpResponse

# Create View
def create_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        email = request.POST.get('email')
        Student.objects.create(name=name, roll=roll, email=email)
        return redirect('list_students')
    return render(request, 'students/create_student.html')

# Read (List) View
def list_students(request):
    students = Student.objects.all()
    return render(request, 'students/list_students.html', {'students': students})

# Update View
def update_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.roll = request.POST.get('roll')
        student.email = request.POST.get('email')
        student.save()
        return redirect('list_students')
    return render(request, 'students/update_student.html', {'student': student})

# Delete View
def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('list_students')
    return render(request, 'students/delete_student.html', {'student': student})