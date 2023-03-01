from django.contrib import admin
from django.urls import path, include
from home import views


urlpatterns = [
    path('', views.index, name= 'home'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),
    path('userProfile', views.userProfile, name='userProfile'),
    path('about', views.about, name='about'),
    path('home-save', views.save, name='home-save'),
    path('Analysis', views.Analysis, name='Analysis'),
]
