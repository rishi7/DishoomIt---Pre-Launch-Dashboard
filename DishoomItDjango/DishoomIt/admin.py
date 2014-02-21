'''
Created on Jan 30, 2014

@author: hrishikeshrajpathak
'''
from DishoomIt.models import Dish
from DishoomIt.models import Restaurant
from DishoomIt.models import Menu
from django.contrib import admin

admin.site.register(Dish)
admin.site.register(Restaurant)
admin.site.register(Menu)
