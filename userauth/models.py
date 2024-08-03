from django.db import models
from django.contrib.auth.models import User
from post.models import Post

# Uploading user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    first_name= models.CharField(max_length=50, null=True, blank=True)
    last_name= models.CharField(max_length=50, null=True, blank=True)
    location= models.CharField(max_length=50, null=True, blank=True)
    url= models.URLField(max_length=200, null=True, blank=True)
    bio= models.TextField(max_length=100, null=True, blank=True)
    image= models.ImageField(upload_to= user_directory_path, blank=True, null=True)
    favourite= models.ManyToManyField(Post)
    
    def __str__(self):
        return self.user.username