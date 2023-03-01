from django.db import models

# Create your models here.
def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return 'images/%s.%s' % (instance.username, extension)  

class UserProfile(models.Model):
    username = models.CharField(max_length=15, primary_key = True)
    email = models.CharField(max_length=30)
    lname = models.CharField(max_length=15)
    fname = models.CharField(max_length=15)
    tid = models.CharField(max_length=15)
    yid = models.CharField(max_length=15)
    image = models.ImageField(upload_to=upload_location, default='')

    def __str__(self):
        return self.username

class Post(models.Model):
    username = models.CharField(max_length=15)
    link = models.CharField(max_length=200)
    pos = models.IntegerField(default=0)
    neg = models.IntegerField(default=0)
    neu = models.IntegerField(default=0)
    time = models.CharField(max_length=20, default='0')

# class Image(models.Model):
#     username = models.CharField(max_length=15, primary_key = True)
#     image = models.ImageField(upload_to='statics', default='')

  