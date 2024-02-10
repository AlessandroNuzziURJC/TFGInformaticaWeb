from django.urls import path
from .views import *

urlpatterns = [
    path('enqueue/', enqueue, name='enqueue'),
    path('get_queue/', get_queue, name='get_queue'),
    path('store_conf_files/', store_conf_files, name='store_conf_files'),
    path('get_yaml_conf_file/', get_yaml_conf_file, name='get_yaml_conf_file'),
    path('exists_yaml_conf_file/', exists_yaml_conf_file, name = 'exists_yaml_conf_file'),
    path('get_sh_conf_file/', get_sh_conf_file, name='get_sh_conf_file'),
    path('exists_sh_conf_file/', exists_sh_conf_file, name = 'exists_sh_conf_file'),
]