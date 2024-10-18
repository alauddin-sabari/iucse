### Django Forms Creation Tutorial

This step-by-step guidelines to cover the basics of Django forms, creating a "Contact Us" form, and integrating it with a MySQL database.

#### Prerequisites
- Basic understanding of Django (installation, setup, project structure).
- MySQL installed and a database ready.
- A Django project setup with MySQL as the database.

### Step 1: Set Up MySQL with Django
First, configure MySQL to work with Django by updating the `settings.py` file.

1. Install `mysqlclient`:
   ```bash
   pip install mysqlclient
   ```

2. Open `settings.py` and configure your database settings:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_database_name',
           'USER': 'your_mysql_user',
           'PASSWORD': 'your_mysql_password',
           'HOST': 'localhost',  
           'PORT': '3306',
       }
   }
   ```

3. Create the MySQL database:
   ```sql
   CREATE DATABASE your_database_name;
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Step 2: Creating a Django App for Forms
1. Create a new Django app to handle the form. Run this command:
   ```bash
   python manage.py startapp contact
   ```

2. Add `'contact'` to the `INSTALLED_APPS` section in `settings.py`.

### Step 3: Creating the Contact Form

1. In the `contact` app directory, create a file called `forms.py`:
   ```bash
   touch contact/forms.py
   ```

2. Define a form inside `forms.py`:
   ```python
   from django import forms

   class ContactForm(forms.Form):
       name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
       email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
       message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
   ```

### Step 4: Creating the View
1. In `views.py` of the `contact` app, create a view to handle the form submission:
   ```python
   from django.shortcuts import render
   from .forms import ContactForm

   def contact_us(request):
       if request.method == 'POST':
           form = ContactForm(request.POST)
           if form.is_valid():
               # Process form data, you could save it to the database
               print(form.cleaned_data)
               # Add logic to save data to MySQL
       else:
           form = ContactForm()

       return render(request, 'contact/contact_us.html', {'form': form})
   ```

### Step 5: Creating the Contact Us Template
1. Inside the `contact` app directory, create a `templates/contact` directory:
   ```bash
   mkdir -p contact/templates/contact
   ```

2. Create a template file called `contact_us.html` inside the `templates/contact` folder:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Contact Us</title>
   </head>
   <body>
       <h1>Contact Us</h1>
       <form method="post">
           {% csrf_token %}
           {{ form.as_p }}
           <button type="submit">Submit</button>
       </form>
   </body>
   </html>
   ```

### Step 6: URL Configuration
1. Add a URL for the contact form in `urls.py`:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('contact/', views.contact_us, name='contact_us'),
   ]
   ```

2. Include this in the project's `urls.py`:
   ```python
   from django.urls import include

   urlpatterns = [
       path('', include('contact.urls')),
   ]
   ```

### Step 7: Saving Form Data to MySQL

You can save the contact form submissions into a MySQL table by creating a model.

1. Define a model inside `models.py`:
   ```python
   from django.db import models

   class Contact(models.Model):
       name = models.CharField(max_length=100)
       email = models.EmailField()
       message = models.TextField()

       def __str__(self):
           return self.name
   ```

2. Create the migration:
   ```bash
   python manage.py makemigrations
   ```

3. Apply the migration:
   ```bash
   python manage.py migrate
   ```

4. Update the view to save the form data to the database:
   ```python
   from .models import Contact

   def contact_us(request):
       if request.method == 'POST':
           form = ContactForm(request.POST)
           if form.is_valid():
               # Save to MySQL database
               contact = Contact(
                   name=form.cleaned_data['name'],
                   email=form.cleaned_data['email'],
                   message=form.cleaned_data['message']
               )
               contact.save()
       else:
           form = ContactForm()

       return render(request, 'contact/contact_us.html', {'form': form})
   ```

### Step 8: Testing the Form
Run the Django development server:
```bash
python manage.py runserver
```

Navigate to `http://localhost:8000/contact/` and test the form submission. Verify that the data is saved in the MySQL database.

 