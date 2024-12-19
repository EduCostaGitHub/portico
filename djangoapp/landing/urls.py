from django.urls import path
from landing.views import index


urlpatterns = [
    path('', index, name='index'),
]
