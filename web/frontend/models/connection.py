from openstack import connection
import yaml
from django.conf import settings
import os

class Openstack_Service():
    max_vcpus = 64
    max_volumes = 12
    max_floating_ip = 2

    conn = None

    def __init__(self) -> None:
        file_path = os.path.join(settings.BASE_DIR, 'frontend/files')
        for file_name in os.listdir(file_path):
            if file_name.endswith('.yaml'):
                with open(file_path + '/' + file_name, 'r') as file:
                    aux = yaml.safe_load(file)
                    clouds = aux['clouds']
                    MDS = clouds['MDS']
                    self.auth = MDS['auth']

    def connect(self):
        self.conn = connection.Connection(**self.auth)

    def disconnect(self):
        self.conn.close()
        self.conn = None

    def flavors(self):
        l = list(self.conn.compute.flavors())
        return list(sorted(l, key=lambda x: int(x.id[1:])))
    
    def get_limits(self):
        return self.conn.get_compute_limits()
    
    def instances_available(self):
        # Get used vcpus
        used_instances = list(self.conn.compute.servers())
        used_vcpus = 0
        for e in used_instances:
            used_vcpus += e.flavor.vcpus

        # Filter valid instances
        flavors_names = []
        for e in list(self.flavors()):
            if ('c' in e.id and int(e.id[1:]) <= self.get_limits()['maxTotalCores'] - used_vcpus):
                flavors_names.append(e.id)
        return flavors_names
       
        
