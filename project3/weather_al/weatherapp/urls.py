from django.urls import path
from .views import index
from .views  import index
urlpatterns = [
    # path('', views.index, name='index'),
    path('', index, name='index'),
]
