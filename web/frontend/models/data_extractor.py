import os
import re
import statistics
from django.conf import settings
from frontend.models.execution import Execution

file_path = os.path.join(settings.BASE_DIR, 'files')


class DataExtractor:
    """
    Clase para extraer y procesar datos de ejecuciones.

    Esta clase se utiliza para extraer datos relevantes de las ejecuciones,
    como tiempos y costos, para su posterior procesamiento y visualización.

    Attributes:
        instances_list (list): Lista de tipos de instancias disponibles.
        prices (dict): Diccionario que almacena los precios de los tipos de instancias.
        execution_unique_name (str): Nombre único de la ejecución.
        execution (Execution): Instancia de la clase Execution para acceder a datos de ejecuciones.
    """

    instances_list = ['c04', 'c08', 'c16', 'c32']

    def __init__(self, execution_unique_name):
        """
        Inicializa la clase DataExtractor con el nombre único de la ejecución.

        Args:
            execution_unique_name (str): Nombre único de la ejecución.
        """

        self.prices = self.extract_prices()
        self.execution_unique_name = execution_unique_name
        self.execution = Execution(execution_unique_name=execution_unique_name)

    def extract_prices(self):
        """
        Extrae los precios de los tipos de instancias desde un archivo.

        Lee el archivo 'prices.txt' y extrae los precios de los tipos de instancias
        para almacenarlos en un diccionario.

        Returns:
            dict: Diccionario que contiene los precios de los tipos de instancias.
        """
        path = os.path.join(
            settings.BASE_DIR, file_path, 'prices.txt')
        output = {}
        with open(path, 'r') as file:
            for line in file:
                divided_line = line.split(': ')
                output[divided_line[0]] = float(divided_line[1])

        return output

    def extract_times(self):
        """
        Extrae los datos de tiempos de una ejecución para su visualización.

        Lee los archivos de resultados de la ejecución y los datos de instalación,
        y los organiza en un formato adecuado para su visualización.

        Returns:
            dict: Diccionario con los datos de tiempos y de instalación.
        """
        output = {}
        files = sorted(os.listdir('./output/' + self.execution_unique_name + '/results'),
                       key=(lambda x: int(re.split('_', x)[1])))
        for file in files:
            aux = []
            with open('./output/' + self.execution_unique_name + '/results/' + file, 'r') as archivo:
                for l in archivo:
                    aux.append(float(l))
            output[re.sub(r'[^a-zA-Z0-9]', '', file[:-4])] = aux

        install = {}
        files_install = sorted(os.listdir(
            './output/' + self.execution_unique_name + '/installation_time'))
        for file in files_install:
            aux = []
            with open('./output/' + self.execution_unique_name + '/installation_time/' + file, 'r') as archivo:
                for l in archivo:
                    aux.append(float(l))
            install[file[:-4]] = aux

        return {'data': output,
                'threads': list(map(lambda x: re.split('_', x)[1], files)),
                'install': install}

    def extract_cost(self):
        """
        Extrae los datos de costos de una ejecución para su visualización.

        Calcula los costos de la ejecución, incluyendo costos de ejecución y de instalación,
        y los organiza en un formato adecuado para su tratamiento en las gráficas.

        Returns:
            dict: Diccionario con los datos de costos.
        """
        output = {'urjc': [],
                  'urjc_installation': [],
                  'threads': 0}

        aux_dict = {}
        files = sorted(os.listdir('./output/' + self.execution_unique_name + '/results'),
                       key=(lambda x: int(re.split('_', x)[1])))
        output['threads'] = list(map(lambda x: re.split('_', x)[1], files))

        for file in files:
            aux = []
            with open('./output/' + self.execution_unique_name + '/results/' + file, 'r') as archivo:
                for l in archivo:
                    aux.append(float(l))
            aux_dict[re.sub(r'[^a-zA-Z0-9]', '', file[:-4])] = aux

        for key, value in aux_dict.items():
            aux = 0
            aux_list = []
            with open('./output/' + self.execution_unique_name + '/installation_time/' + key + '.txt', 'r') as text_file:
                aux = float(text_file.readline())
                output['urjc'].append(
                    round(self.prices[key] / 3600 * statistics.mean(value), 9))
                for elem in value:
                    aux_list.append(elem + aux)
                output['urjc_installation'].append(
                    round(self.prices[key] / 3600 * statistics.mean(aux_list), 9))

        return output
