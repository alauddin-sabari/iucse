Guideline for implementing CRUD (Create, Read, Update, Delete) operations in Django using a **Student** table with fields `name`, `roll`, and `email`. This guide will help you prepare for your lecture on Django Project 1.

### **Step 1: Set Up the Django Project and App**

1. **Create a Django project** if you haven’t already:
   ```bash
   django-admin startproject student_crud
   cd student_crud
   ```

2. **Create a new app** called `students`:
   ```bash
   python manage.py startapp students
   ```

3. **Add the app to `INSTALLED_APPS`** in `student_crud/settings.py`:
   ```python
   INSTALLED_APPS = [
       # other apps
       'students',
   ]
   ```

### **Step 2: Create the Student Model**

In `students/models.py`, create the `Student` model with the fields `name`, `roll`, and `email`.

```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
```

### **Step 3: Migrate the Database**

1. Create the migration file for the `Student` model:
   ```bash
   python manage.py makemigrations
   ```

2. Apply the migration to create the `Student` table in the database:
   ```bash
   python manage.py migrate
   ```

### **Step 4: Create CRUD Views**

In `students/views.py`, write views for creating, reading, updating, and deleting student records.

```python
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
```

### **Step 5: Create URL Patterns**

In `students/urls.py`, define the URL patterns for the CRUD views.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_student, name='create_student'),
    path('', views.list_students, name='list_students'),
    path('update/<int:student_id>/', views.update_student, name='update_student'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
]
```

Don’t forget to include the `students` app URLs in the project’s main `urls.py` file:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
]
```

### **Step 6: Create Templates**

1. **Create a directory called `templates` inside the `students` app** and subdirectories like this:
   ```bash
   students/
   └── templates/
       └── students/
           ├── create_student.html
           ├── list_students.html
           ├── update_student.html
           └── delete_student.html
   ```

2. **Template: `create_student.html`**

```html
<h2>Create Student</h2>
<form method="POST">
    {% csrf_token %}
    <label for="name">Name:</label><br>
    <input type="text" name="name"><br><br>

    <label for="roll">Roll:</label><br>
    <input type="number" name="roll"><br><br>

    <label for="email">Email:</label><br>
    <input type="email" name="email"><br><br>

    <button type="submit">Create</button>
</form>
<a href="{% url 'list_students' %}">Back to List</a>
```

3. **Template: `list_students.html`**

```html
<h2>List of Students</h2>
<table>
    <tr>
        <th>Name</th>
        <th>Roll</th>
        <th>Email</th>
        <th>Actions</th>
    </tr>
    {% for student in students %}
    <tr>
        <td>{{ student.name }}</td>
        <td>{{ student.roll }}</td>
        <td>{{ student.email }}</td>
        <td>
            <a href="{% url 'update_student' student.id %}">Edit</a>
            <a href="{% url 'delete_student' student.id %}">Delete</a>
        </td>
    </tr>
    {% endfor %}
</table>
<a href="{% url 'create_student' %}">Add New Student</a>
```

4. **Template: `update_student.html`**

```html
<h2>Update Student</h2>
<form method="POST">
    {% csrf_token %}
    <label for="name">Name:</label><br>
    <input type="text" name="name" value="{{ student.name }}"><br><br>

    <label for="roll">Roll:</label><br>
    <input type="number" name="roll" value="{{ student.roll }}"><br><br>

    <label for="email">Email:</label><br>
    <input type="email" name="email" value="{{ student.email }}"><br><br>

    <button type="submit">Update</button>
</form>
<a href="{% url 'list_students' %}">Back to List</a>
```

5. **Template: `delete_student.html`**

```html
<h2>Are you sure you want to delete {{ student.name }}?</h2>
<form method="POST">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
</form>
<a href="{% url 'list_students' %}">Cancel</a>
```

### **Step 7: Test the CRUD Functionality**

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to `http://localhost:8000/students/` to see the list of students and try out the Create, Read, Update, and Delete functionalities.

### **Summary**

- **Create**: Add a new student using a form.
- **Read**: View a list of students.
- **Update**: Modify student information.
- **Delete**: Remove a student from the database.

 