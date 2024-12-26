from django.urls import path

from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.index, name='index'),

    # contact (CRUD)
    path('contact/<int:contact_id>/detail/', views.contact, name='contact'),
    path('contact/create/', views.create, name='create'),
    path('contact/<int:contact_id>/update/', views.update, name='update'),
    path('contact/<int:contact_id>/delete/', views.delete, name='delete'),


    # user
    path('create/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update/', views.user_update, name='user_update'),
]
