from openstack import connection

class Openstack_Service():
    # Configuración de las credenciales de OpenStack
    auth = {
        'auth_url': 'https://clea.etsii.urjc.es:5000/v3/',
        'project_name': 'fg-arqdistr',
        'username': 'fg-arqdistr',
        'password': '/dB3lGoqMMb6jbyd',
        'user_domain_name': 'Default',
        'project_domain_name': 'Default',
    }
    max_vcpus = 64
    max_volumes = 12
    max_floating_ip = 2

    conn = None

    def connect(self):
        self.conn = connection.Connection(**self.auth)

    def disconnect(self):
        self.conn.close()
        self.conn = None

    def flavors(self):
        l = list(self.conn.compute.flavors())
        return list(sorted(l, key=lambda x: int(x.id[1:])))
    
    def free_vcpus(self):
        #user = self.conn.identity.find_user(username='fg-arqdistr', domain_name='Default')

        used_instances = list(self.conn.compute.servers())
        used_vcpus = 0
        for e in used_instances:
            used_vcpus += e.flavor.vcpus
        return self.max_vcpus - used_vcpus
    
    def instances_available(self):
        # Get used vcpus
        used_instances = list(self.conn.compute.servers())
        used_vcpus = 0
        for e in used_instances:
            used_vcpus += e.flavor.vcpus

        # Filter valid instances
        flavors_names = []
        for e in list(self.flavors()):
            if ('c' in e.id and int(e.id[1:]) <= self.max_vcpus - used_vcpus):
                flavors_names.append(e.id)
        return flavors_names
       
        
