from django.shortcuts import render, HttpResponse
import requests

# Create your views here.

def index(request):
    # return HttpResponse("Weather app")
    if 'city' in request.GET:
        city = request.GET['city']
        data = get_weather(city)
    else:
        data = {}
    # return render(request, 'index.html', {'data': data})
    return render(request, 'index1.html', {'data': data})

def get_weather(city):
    api_key = 'f26ec7b52c76ec0bca498385c91716b8'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    # Extract country code and temperature in Celsius
    country_code = data['sys']['country']
    temperature_kelvin = data['main']['temp']
    temperature_celsius = temperature_kelvin - 273.15
    # temperature_celsius = round(temperature_celsius, 2)
    # Add country code and temperature in Celsius to the response data
    data['country_code'] = country_code
    data['temperature_celsius'] = temperature_celsius 
    return data