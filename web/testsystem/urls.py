from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('executions/', executions, name='executions'),
    path('index_form/', form, name='form'),
    path('queue/', queue, name='queue'),
    path('configuration/', configuration, name='configuration')
]
