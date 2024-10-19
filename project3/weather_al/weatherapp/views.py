from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    if 'city' in request.GET:
        city = request.GET['city']
        weather_details = get_weather(city)
    else:
        weather_details = {}
    
    # return HttpResponse("Weather app")
    return render(request, 'index.html', {'data': weather_details}) 

import requests

def get_weather(city):
    api_key = '668678aa9e3105acd88d5a26266c0a3d'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    # Extract country code and temperature in Celsius
    country_code = data['sys']['country']
    temperature_kelvin = data['main']['temp']
    temperature_celsius = temperature_kelvin - 273.15
    temperature_celsius = round(temperature_celsius, 2)
    # Add country code and temperature in Celsius to the response data
    data['country_code'] = country_code
    data['temperature_celsius'] = temperature_celsius 
    return data