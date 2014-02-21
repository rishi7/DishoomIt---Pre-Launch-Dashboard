from django.conf.urls import patterns, include, url
import autocomplete_light
# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DishoomItDjango.views.home', name='home'),
    # url(r'^index/$', include('DishoomIt.views.index')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'DishoomIt.views.index'),
    url(r'^index/$', 'DishoomIt.views.index'),
    
    url(r'^login/$', 'DishoomIt.views.login'),
    url(r'^auth/$', 'DishoomIt.views.auth_view'),
    url(r'^logout/$', 'DishoomIt.views.logout'),
    #url(r'^loggedin/$', 'DishoomIt.views.loggedin'),
    url(r'^invalid/$', 'DishoomIt.views.invalid_login'),
    
    url(r'^starts_with/(?P<alphabet>.+)/dish/(?P<dish_id>\d+)/$', 'DishoomIt.views.alphabet_dish'),
    url(r'^starts_with/(?P<alphabet>.+)/$', 'DishoomIt.views.alphabet'),
    url(r'^submit/$', 'DishoomIt.views.submit'),
    url(r'^auto/', include('autocomplete_light.urls')),
    
)
