'''
Created on Feb 3, 2014

@author: hrishikeshrajpathak
'''

from django import forms

import autocomplete_light

from .models import Restaurant

RATING_CHOICES = (
     ('1', "--"),
     ('2', "1 (very bad)"),
     ('3', "2 (bad)"),
     ('4', "3 (average)"),
     ('5', "4 (good)"),
     ('6', "5 (excellent)"),
 )


class RestaurantForm(forms.Form):
    restaurant = forms.ModelChoiceField(
                    Restaurant.objects.all(),
                    label="Restaurant Name",
                    widget=autocomplete_light.ChoiceWidget(
                       'RestaurantAutocomplete',
                        attrs={
                            'class':'form-control',
                            'style':'width:100%;',
                            'id':'restaurant'
                            }
                        )
                    )
    menu_name = forms.CharField(label='Name on Menu (optional)', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    rating = forms.ChoiceField(label='Rating', choices=RATING_CHOICES,
                               widget=forms.Select(attrs={'class':'form-control'}))


class RestaurantFormNew(forms.Form):
    restaurant = forms.CharField(label='Restaurant Name', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control', 'id':'restaurant'}))
    menu_name = forms.CharField(label='Name on Menu (optional)', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    street = forms.CharField(label='Street (optional)', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    area = forms.CharField(label='Area', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    rating = forms.ChoiceField(label='Rating', choices=RATING_CHOICES,
                               widget=forms.Select(attrs={'class':'form-control'}))
    

class DishForm(forms.Form):
    dish_name = forms.CharField(label='Dish Name', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    restaurant = forms.ModelChoiceField(
                    Restaurant.objects.all(),
                    label="Restaurant Name",
                    widget=autocomplete_light.ChoiceWidget(
                       'RestaurantAutocomplete',
                        attrs={
                            'class':'form-control',
                            'style':'width:100%;',
                            'id':'restaurant'
                            }
                        )
                    )
    menu_name = forms.CharField(label='Name on Menu (optional)', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    rating = forms.ChoiceField(label='Rating', choices=RATING_CHOICES,
                               widget=forms.Select(attrs={'class':'form-control'}))
    
    
class DishFormNew(forms.Form):
    dish_name = forms.CharField(label='Dish Name', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    restaurant = forms.CharField(label='Restaurant Name', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control', 'id':'restaurant'}))
    menu_name = forms.CharField(label='Name on Menu (optional)', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    street = forms.CharField(label='Street (optional)', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    area = forms.CharField(label='Area', max_length=64,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    rating = forms.ChoiceField(label='Rating', choices=RATING_CHOICES,
                               widget=forms.Select(attrs={'class':'form-control'}))
