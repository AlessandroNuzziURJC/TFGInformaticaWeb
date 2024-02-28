import os
import statistics as stats
import re
from testsystem.models.execution import Execution


class DataExtractor:

    prices = {'c04': [0.02, 0.01, 0.004], 'c08': [0.04, 0.02, 0.008], 'c16': [
    0.08, 0.04, 0.016], 'c32': [0.16, 0.08, 0.032]}
    instances_list = ['c04', 'c08', 'c16', 'c32']
    #times = {'c04': 131.90803937117258, 'c08': 145.78145890235902, 'c16': 146.31223859786988, 'c32': 146.45875180562336}
    times = {'c04': 105.3, 'c08': 118.067, 'c16': 118.3, 'c32': 119.2}

    def __init__(self, execution_unique_name):
        self.execution_unique_name = execution_unique_name
        self.execution = Execution(execution_unique_name=execution_unique_name)

    def extract_times(self):
        """
        Trata los datos de tiempos de una ejecucion para la grafica en Javascript.

        Args:

        Returns:
            Devuelve un diccionario con los datos.
        """
        output = []
        std_dev = [0]
        files = sorted(os.listdir('./output/' + self.execution_unique_name + '/results'),
                       key=(lambda x: int(re.split('_', x)[1])))
        for file in files:
            aux = []
            with open('./output/' + self.execution_unique_name + '/results/' + file, 'r') as archivo:
                for l in archivo:
                    aux.append(float(l))
            output.append(stats.mean(aux))
            if len(aux) > 1:
                std_dev.append(stats.stdev(aux))
            else:
                std_dev.append(0)

        return {'data': output, 'threads': list(
            map(lambda x: re.split('_', x)[1], files)), 'std_dev': std_dev}
    
    def extract_cost(self):
        """
        Trata los datos de costes de una ejecucion para la grafica en Javascript.

        Args:

        Returns:
            Devuelve un diccionario con los datos.
        """
        output = {}
        values = self.extract_times()
        output['threads'] = values['threads']
        output['data'] = {'urjc': []}

        aux = 0
        if not self.execution.MPI:
            aux += 1
        i = 1
        if len(values['data']) == 1:
            return {}

        for elem in values['data']:
            if i >= 1 and i <= 3 + aux:
                flavor = 'c04'
            elif i >= 4 and i <= 7 + aux:
                flavor = 'c08'
            elif i >= 8 and i <= 15 + aux:
                flavor = 'c16'
            else:
                flavor = 'c32'
            value = (elem + self.times[flavor]) / 3600
            i += 1    
            
            #output['data']['private_company'].append(round(self.prices[flavor][0] * value, 9))
            #output['data']['official_organization'].append(round(self.prices[flavor][1] * value, 9))
            output['data']['urjc'].append(round(self.prices[flavor][2] * value, 9))
            

        return output

