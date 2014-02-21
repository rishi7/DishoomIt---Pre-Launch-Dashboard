from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Dish(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
    
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    area = models.CharField(max_length=50)
    street = models.CharField(max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    
class Menu(models.Model):
    rating = models.IntegerField()
    name = models.CharField(max_length=100, null=True, blank=True)
    dish_ref = models.ForeignKey(Dish)
    rest_ref = models.ForeignKey(Restaurant) 
    user_ref = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.dish_ref

