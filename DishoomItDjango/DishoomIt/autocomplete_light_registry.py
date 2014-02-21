'''
Created on Feb 3, 2014

@author: hrishikeshrajpathak
'''
import autocomplete_light

from .models import Restaurant

class RestaurantAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^name']
    autocomplete_js_attributes = {
        # This will actually data-autocomplete-minimum-characters which
        # will set widget.autocomplete.minimumCharacters.
        'minimum_characters'  : 3,
        'placeholder'         : 'Enter the name of a restaurant...',
        # 'class'               : 'form-control',
        # 'style'               : 'width:100%;'
    }

    widget_js_attributes = {
        # That will set data-max-values which will set widget.maxValues
        'max_values': 1,
    }

autocomplete_light.register(Restaurant, RestaurantAutocomplete)
