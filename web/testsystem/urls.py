from django.urls import path
from .views.index_view import *
from .views.executions_view import *
from .views.configuration_views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('executions/', executions, name='executions'),
    path('index_form/', form, name='form'),
    path('queue/', queue, name='queue'),
    path('configuration/', configuration, name='configuration'),
    path('yaml_config_file/', yaml_config_file, name='yaml_config_file'),
    path('script_config_file', script_config_file, name='script_config_file')
]
