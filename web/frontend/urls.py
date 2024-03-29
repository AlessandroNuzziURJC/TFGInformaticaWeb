from django.urls import path
from .views.index_view import *
from .views.executions_view import *
from .views.configuration_views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('executions/', executions, name='executions'),
    path('cards/', cards_list, name='cards_list'),
    path('index_form/', form, name='form'),
    path('configuration/', configuration, name='configuration'),
    path('executions/delete/<str:execution_unique_name>', delete_execution, name='delete_execution'),
    path('executions/<str:execution_unique_name>', execution, name='execution'),
    path('datafiles/<str:execution_unique_name>', datafiles, name="datafiles"),
    path('data/times/<str:execution_unique_name>', data_times, name='data_times'),
    path('data/costs/<str:execution_unique_name>', data_costs, name='data_costs'),
    path('configuration/prices', price_file, name='price_file'),
]
