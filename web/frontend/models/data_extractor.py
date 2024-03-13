import os
import re
import statistics
from django.conf import settings
from frontend.models.execution import Execution

file_path = os.path.join(settings.BASE_DIR, 'frontend/files')

class DataExtractor:

    instances_list = ['c04', 'c08', 'c16', 'c32']
    #times = {'c04': 131.90803937117258, 'c08': 145.78145890235902, 'c16': 146.31223859786988, 'c32': 146.45875180562336}
    times = {'c04': 105.3, 'c08': 118.067, 'c16': 118.3, 'c32': 119.2}

    def __init__(self, execution_unique_name):
        self.prices = self.extract_prices()
        self.execution_unique_name = execution_unique_name
        self.execution = Execution(execution_unique_name=execution_unique_name)

    def extract_prices(self):
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
        Trata los datos de tiempos de una ejecucion para la grafica en Javascript.

        Args:

        Returns:
            Devuelve un diccionario con los datos.
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
        files_install = sorted(os.listdir('./output/' + self.execution_unique_name + '/installation_time'))
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
        Trata los datos de costes de una ejecucion para la grafica en Javascript.

        Args:

        Returns:
            Devuelve un diccionario con los datos.
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
                output['urjc'].append(round(self.prices[key] / 3600 * statistics.mean(value), 9))
                for elem in value:
                    aux_list.append(elem + aux)
                output['urjc_installation'].append(round(self.prices[key] / 3600 * statistics.mean(aux_list), 9))

        return output

