from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField, ImageField


class User(AbstractUser):
  image = models.ImageField(upload_to='users_images', blank=True, 
                            null=True, verbose_name="Аватар")
  phone_number = models.CharField(max_length=11, blank=True, null=True,)

  class Meta:
    db_table = 'user'            
    verbose_name = 'Пользователя'
    verbose_name_plural = 'Пользователи'

    def __str__(self): # what you will see in admin panel
         return self.username
    

