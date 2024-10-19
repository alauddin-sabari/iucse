# charts/urls.py
from django.urls import path
from .views import bar_chart

urlpatterns = [
    path('bar/', bar_chart, name='bar_chart'),
]
