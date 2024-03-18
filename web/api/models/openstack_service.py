from openstack import connection
import yaml
from django.conf import settings
import os

class OpenstackService():
    """
    Clase para interactuar con servicios de OpenStack.

    Atributos:
        conn (openstack.connection.Connection): Conexión a OpenStack.
        auth (dict): Credenciales de autenticación para la conexión.
    """

    conn = None

    def __init__(self) -> None:
        """
        Inicializa la instancia de OpenstackService.
        """
        file_path = os.path.join(settings.BASE_DIR, 'api/files')
        for file_name in os.listdir(file_path):
            if file_name.endswith('.yaml'):
                with open(file_path + '/' + file_name, 'r') as file:
                    aux = yaml.safe_load(file)
                    clouds = aux['clouds']
                    MDS = clouds['MDS']
                    self.auth = MDS['auth']

    def connect(self):
        """
        Conecta con OpenStack.
        """
        self.conn = connection.Connection(**self.auth)

    def disconnect(self):
        """
        Desconecta de OpenStack.
        """
        self.conn.close()
        self.conn = None

    def flavors(self):
        """
        Obtiene la lista de flavors disponibles en OpenStack.

        Returns:
            list: Lista de flavors.
        """
        l = list(self.conn.compute.flavors())
        return list(sorted(l, key=lambda x: int(x.id[1:])))

    def get_limits(self):
        """
        Obtiene los límites de recursos en OpenStack.

        Returns:
            dict: Límites de recursos.
        """
        return self.conn.get_compute_limits()

    def instances_available(self):
        """
        Obtiene los nombres de los sabores disponibles considerando los límites de vCPUs.

        Returns:
            list: Lista de nombres de sabores disponibles.
        """
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
    
    def find_vcpus_used_in_flavor(self, flavor_name):
        """
        Busca el número de vCPUs utilizadas en un sabor dado.

        Args:
            flavor_name (str): Nombre del sabor.

        Returns:
            str: Número de vCPUs utilizadas.
        """
        return str(self.conn.compute.find_flavor(flavor_name)['vcpus'])

    def create_key(self, path, name):
        """
        Crea una clave de SSH y la guarda en un archivo.

        Args:
            path (str): Ruta donde se guardará la clave.
            name (str): Nombre de la clave.
        """
        keypair = self.conn.compute.find_keypair(name)

        if keypair:
            self.conn.compute.delete_keypair(name)

        keypair = self.conn.compute.create_keypair(name=name)
        
        with open(path, 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod(path, 0o400)
