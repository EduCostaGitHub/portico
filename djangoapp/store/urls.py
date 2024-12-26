from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    # product
    path('', views.index, name='index'),



    # request


    # profile

]
