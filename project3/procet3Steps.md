To add a **user interface (UI)** that allows users to input a location (city name or coordinates) and fetch the weather forecast for that area, we'll make some changes to the Django project. We'll build a form where users can input the city name, convert that into latitude and longitude using OpenWeatherMap's **Geocoding API**, and then fetch the weather data.

### Changes to Implement:
1. **Create a Form for User Input**
2. **Use Geocoding API to Convert City to Coordinates**
3. **Fetch and Display Weather Data Based on User Input**
4. **Display Plotly Chart in the Template**

---

### Step 1: **Create a Form for User Input**

We need a form where the user can input a city name, and then we can use this city name to get the coordinates (latitude and longitude) required for the weather data.

#### 1. Create a Form in Django

In `weather/forms.py`, create a form to take user input for the city name.

```python
# weather/forms.py
from django import forms

class LocationForm(forms.Form):
    city_name = forms.CharField(label='City Name', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter city name'
    }))
```

- **`forms.CharField`**: This is a text input where the user enters the name of the city.
- **`widget=forms.TextInput`**: Adds a bit of styling using Bootstrap classes for better UI.

#### 2. Update `weather/views.py` to Handle User Input

We need to modify the view to render the form and handle the data submitted by the user.

```python
# weather/views.py
import requests
from django.shortcuts import render
from .forms import LocationForm
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime

# Define your OpenWeatherMap API key
API_KEY = 'your_openweathermap_api_key'

def get_coordinates(city_name):
    """Use OpenWeatherMap's Geocoding API to get the coordinates of a city"""
    geocode_url = 'http://api.openweathermap.org/geo/1.0/direct'
    params = {
        'q': city_name,
        'limit': 1,  # We only want the top result
        'appid': API_KEY
    }
    response = requests.get(geocode_url, params=params)
    data = response.json()
    
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    return None, None

def weather_chart(request):
    form = LocationForm()
    graph_html = None

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            lat, lon = get_coordinates(city_name)
            
            if lat and lon:
                # Fetch weather data for the given coordinates
                weather_url = 'https://api.openweathermap.org/data/2.5/onecall'
                params = {
                    'lat': lat,
                    'lon': lon,
                    'exclude': 'current,minutely,hourly',
                    'appid': API_KEY,
                    'units': 'metric'
                }
                response = requests.get(weather_url, params=params)
                weather_data = response.json()
                
                # Process the weather data
                dates = []
                temperatures = []
                humidity = []
                
                for day in weather_data['daily']:
                    date = datetime.utcfromtimestamp(day['dt']).strftime('%Y-%m-%d')
                    dates.append(date)
                    temperatures.append(day['temp']['day'])
                    humidity.append(day['humidity'])
                
                # Create Plotly chart
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                    subplot_titles=("Temperature Over a Week", "Humidity Over a Week"))
                
                # Line chart for temperature
                temp_trace = go.Scatter(x=dates, y=temperatures, mode='lines+markers', name='Temperature (°C)')
                fig.add_trace(temp_trace, row=1, col=1)
                
                # Line chart for humidity
                hum_trace = go.Scatter(x=dates, y=humidity, mode='lines+markers', name='Humidity (%)')
                fig.add_trace(hum_trace, row=2, col=1)
                
                fig.update_layout(title_text=f"7-Day Weather Forecast for {city_name}", height=600, width=800)
                
                # Convert the plot to HTML
                graph_html = fig.to_html(full_html=False)
    
    return render(request, 'weather/weather_chart.html', {'form': form, 'graph_html': graph_html})
```

#### Explanation of Changes:

1. **LocationForm**: The form is rendered and processed based on user input.
2. **get_coordinates()**: A helper function that uses OpenWeatherMap's **Geocoding API** to convert the user’s city input into latitude and longitude.
3. **weather_chart()**: Now accepts user input for the city, gets the coordinates, and then fetches the weather data based on those coordinates.

---

### Step 2: **Create a Template for the User Interface**

Now we need a template to display the form and the weather forecast results.

Create the `weather_chart.html` template in the `templates/weather/` directory.

```html
<!-- templates/weather/weather_chart.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Forecast</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="mt-4">Get 7-Day Weather Forecast</h1>
        
        <form method="POST">
            {% csrf_token %}
            <div class="form-group">
                {{ form.city_name.label_tag }}
                {{ form.city_name }}
            </div>
            <button type="submit" class="btn btn-primary">Get Forecast</button>
        </form>
        
        {% if graph_html %}
        <h3 class="mt-5">Weather Forecast</h3>
        <div>
            {{ graph_html|safe }}
        </div>
        {% endif %}
    </div>
</body>
</html>
```

### Explanation:

- **`{% csrf_token %}`**: A security token to prevent CSRF attacks in Django forms.
- **`{{ form.city_name }}`**: Renders the form field for city name input.
- **`{{ graph_html|safe }}`**: Safely renders the Plotly graph HTML if it’s available after the form submission.

---

### Step 3: **Update URL Configuration**

In `weather/urls.py`, make sure the routing points to the weather view.

```python
# weather/urls.py
from django.urls import path
from .views import weather_chart

urlpatterns = [
    path('weather/', weather_chart, name='weather_chart'),
]
```

---

### Step 4: **Run and Test**

1. Run the Django development server:

```bash
python manage.py runserver
```

2. Open `http://127.0.0.1:8000/weather/` in your browser.

You should now see a form where you can enter a city name. After submitting the form, it will display a 7-day weather forecast for that city using Plotly graphs for temperature and humidity.

---

### Final Summary:

1. We added a **form** for user input to get the city name.
2. We used **OpenWeatherMap's Geocoding API** to convert the city name into latitude and longitude.
3. The **weather forecast** was fetched using the latitude and longitude and displayed using **Plotly**.
4. Users can now enter any city to see its 7-day weather forecast. 

 