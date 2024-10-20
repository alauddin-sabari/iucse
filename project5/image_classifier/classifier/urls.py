from django.urls import path
from .views import classify_image

urlpatterns = [
    path('upload/', classify_image, name='upload'),
]
