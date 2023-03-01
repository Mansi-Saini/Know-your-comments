from django.db import models  
from django.forms import fields  
from .models import UserProfile
from django import forms  
  
  
class UserImage(forms.ModelForm):  
    class meta:  
        # To specify the model to be used to create form  
        models = UserProfile 
        # It includes all the fields of model  
        fields = '__all__'  