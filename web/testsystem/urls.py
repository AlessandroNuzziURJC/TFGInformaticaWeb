from django.urls import path
from .views.index_view import *
from .views.executions_view import *
from .views.configuration_views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('executions/', executions, name='executions'),
    path('index_form/', form, name='form'),
    path('configuration/', configuration, name='configuration'),
]
