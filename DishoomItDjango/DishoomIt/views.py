'''
Created on Feb 13, 2014

@author: hrishikeshrajpathak
'''
# # Create your views here.
from DishoomIt.models import *
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.template import Context, RequestContext
from django.template.loader import get_template
import django.views.decorators.csrf
from django.contrib import auth

from .forms import *

alphabet_array = ['All', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# simple login
def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

# authentication module. proceed to index page if successful else go to invalid_login. 
# Think about the option to redirect to login again if not authenticated (with some msg of course)
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/index')
    else:
        return HttpResponseRedirect('/invalid')
    
    
def invalid_login(request):
    return render_to_response('invalid_login.html')


# logout. Redirecting to login page when logout is clicked.
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')


# This is a special case where no alphabet is clicked on by the user. So redirecting it to the generic 
# function with speccific argument 
def index(request):
    # global alphabet_array
    if request.user.is_authenticated():
        return HttpResponseRedirect('/starts_with/%s' % 'All')
    else:
        return HttpResponseRedirect('/login')
    

# Called when user clicks on any option between All to Z on the left hand side on the page.
def alphabet(request, alphabet):
    # global alphabet_array
    user_msg = __get_user_histoty__(request.user)
    if request.user.is_authenticated():
        if alphabet not in alphabet_array:
            alphabet = 'All'
        dishes = __get_dishes_by_alphabet__(alphabet)
        if not dishes:
            return __no_dish__(request, alphabet)   
        active_id = dishes[0].id
        form = RestaurantForm()
        sidebarform = DishForm()
        menus = __get_previous_dish_ratings__(active_id)
        context = {'menus':menus, 'dishes':dishes, 'active_id':active_id, 'alphabet':alphabet, 'array':alphabet_array, 'usernamee':request.user.username, 'form':form, 'sidebarform':sidebarform, 'mainformtype':'rest', 'autocomplete':'true', 'user_msg':user_msg}
        context.update(csrf(request))
        return render(request, 'index.html', context)
    else:
        return HttpResponseRedirect('/login')
    
# Called when user clicks on any specific dish to enter data
def alphabet_dish(request, alphabet, dish_id):
    # global alphabet_array
    user_msg = __get_user_histoty__(request.user)
    if request.user.is_authenticated():
        dishes = __get_dishes_by_alphabet__(alphabet) 
        form = RestaurantForm()
        sidebarform = DishForm()
        menus = __get_previous_dish_ratings__(int(dish_id))
        context = {'menus':menus, 'dishes':dishes, 'active_id':int(dish_id), 'alphabet':alphabet, 'array':alphabet_array, 'usernamee':request.user.username, 'form':form, 'sidebarform':sidebarform, 'mainformtype':'rest', 'autocomplete':'true' , 'user_msg':user_msg}
        context.update(csrf(request))
        return render(request, 'index.html', context)
    else:
        return HttpResponseRedirect('/login')
    

def __no_dish__(request, alphabet):
    user_msg = __get_user_histoty__(request.user)
    form = DishForm()
    sidebarform = DishForm()
    context = {'alphabet':alphabet, 'array':alphabet_array, 'usernamee':request.user.username, 'form':form, 'mainformtype':'dish', 'sidebarform':sidebarform, 'autocomplete':'true' , 'user_msg':user_msg}
    return render(request, 'no-dish.html', context)


def submit(request):
    alphabet = request.POST.get('alphabet').strip()
    location = request.POST.get('location').strip()
    dish_name = request.POST.get('dish_name')
    area_name = request.POST.get('area')
    rating = request.POST.get('rating')
    
    if dish_name:
        return __process_dish_form__(request, alphabet, area_name, rating, location, dish_name)
    else:
        return __process_form__(request, alphabet, area_name, rating, location)


def __process_dish_form__(request, alphabet, area_name, rating, location, dish_name):
    context = {'alphabet':alphabet, 'array':alphabet_array, 'usernamee':request.user.username}
    rest_name_auto = request.POST.get('restaurant', False)
    rest_name_non_auto = request.POST.get('restaurant-autocomplete', False)
    street = request.POST.get('street')
    user_msg = __get_user_histoty__(request.user)
    
    if rest_name_auto == False and area_name is None:
        
        active_id = request.POST.get('active_id').strip()
        dishes = __get_dishes_by_alphabet__(alphabet)
        context['dishes'] = dishes
        context['active_id'] = active_id
        
        if location == 'main':
            context['error'] = 'Entering new restaurant? Help us with address'
            context['sidebarform'] = DishForm()
            context['form'] = DishFormNew({'restaurant': rest_name_non_auto, 'rating':rating, 'dish_name':dish_name, 'user_msg':user_msg})
            return render(request, 'index.html', context)
        else:
            context['sideerror'] = 'Entering new restaurant? Help us with address'
            context['form'] = RestaurantForm()
            context['sidebarform'] = DishFormNew({'restaurant': rest_name_non_auto, 'rating':rating, 'dish_name':dish_name , 'user_msg':user_msg})
            return render(request, 'index.html', context)
    elif rest_name_auto != False and area_name is not None:
        active_id = __save_dish_to_new_rest__(rest_name_auto, street, area_name, dish_name, rating, request.user)
        return HttpResponseRedirect('/starts_with/%s/dish/%s' % (alphabet, active_id))
    else:
        active_id = __save_dish_to_old_rest__(rest_name_auto, dish_name, rating, request.user)
        context['active_id'] = active_id
        return HttpResponseRedirect('/starts_with/%s/dish/%s' % (alphabet, active_id))
    

def __process_form__(request, alphabet, area_name, rating, location):
    context = {'alphabet':alphabet, 'array':alphabet_array, 'usernamee':request.user.username}
    rest_name_auto = request.POST.get('restaurant', False)
    rest_name_non_auto = request.POST.get('restaurant-autocomplete', False)
    active_id = request.POST.get('active_id').strip()
    street = request.POST.get('street')
    user_msg = __get_user_histoty__(request.user)

    
    if rest_name_auto == False and area_name is None:
        context['error'] = 'Entering new restaurant? Help us with address'
        active_id = request.POST.get('active_id').strip()
        dishes = __get_dishes_by_alphabet__(alphabet)
        context['dishes'] = dishes
        context['active_id'] = active_id
        context['sidebarform'] = DishForm()
        context['form'] = RestaurantFormNew({'restaurant': rest_name_non_auto, 'rating':rating, 'user_msg':user_msg})
        return render(request, 'index.html', context)
    elif rest_name_auto != False and area_name is not None:
        __save_to_new_rest__(rest_name_auto, street, area_name, active_id, rating, request.user)
        context['active_id'] = active_id
        return HttpResponseRedirect('/starts_with/%s/dish/%s' % (alphabet, active_id))
    else:
        __save_to_old_rest__(rest_name_auto, active_id, rating, request.user)
        context['active_id'] = active_id
        return HttpResponseRedirect('/starts_with/%s/dish/%s' % (alphabet, active_id))    

        

def __save_dish_to_old_rest__(rest_name_autocomplete, dish_name, rating, user):
    dish = Dish()
    dish.name = dish_name
    dish.save()
    restaurant = Restaurant.objects.get(pk=int(rest_name_autocomplete))
    __save_menu__(restaurant, dish, rating, user)
    return dish.pk

def __save_dish_to_new_rest__(rest_name_new, street, area, dish_name, rating, user):
    dish = Dish()
    dish.name = dish_name
    dish.save()
    restaurant = Restaurant()
    restaurant.area = area
    restaurant.name = rest_name_new
    restaurant.street = street
    restaurant.save()
    __save_menu__(restaurant, dish, rating, user)
    return dish.pk


def __get_previous_dish_ratings__(dish_id):
    menus = Menu.objects.filter(dish_ref__pk=dish_id).order_by('-pk')[:2]
    return menus

def __save_to_old_rest__(restaurant, dish, rating, user):
    dish = Dish.objects.get(pk=int(dish))
    restaurant = Restaurant.objects.get(pk=int(restaurant))
    __save_menu__(restaurant, dish, rating, user)
    
    
def __save_to_new_rest__(restaurant_name, street, area, dish, rating, user):
    dish = Dish.objects.get(pk=int(dish))
    restaurant = Restaurant()
    restaurant.area = area
    restaurant.name = restaurant_name
    restaurant.street = street
    restaurant.save()
    __save_menu__(restaurant, dish, rating, user)
    
    
def __save_menu__(restaurant, dish, rating, user):
    menu = Menu()
    menu.dish_ref = dish
    menu.rest_ref = restaurant
    menu.rating = int(rating) - 1
    menu.user_ref = user
    menu.save()


def __get_dishes_by_alphabet__(alphabet):
    if(alphabet == 'All'):
        dishes = Dish.objects.all().order_by('name')
    else:
        dishes = Dish.objects.filter(name__istartswith=alphabet).order_by('name')
        
    return dishes

def __get_user_histoty__(user):
    count = Menu.objects.filter(user_ref=user).count()
    if count == 0:
        return 'You have not rated any dishes yet.'
    else:
        return '%s dishes rated' % count
