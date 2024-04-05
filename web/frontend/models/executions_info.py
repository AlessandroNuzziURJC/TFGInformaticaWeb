import os


class ExecutionsInfo:
    """
    Clase para obtener información básica de todas las ejecuciones realizadas.

    Esta clase permite extraer los datos básicos de todas las ejecuciones realizadas
    y organizarlos en una lista para su posterior uso.

    Attributes:
        No tiene atributos.
    """

    def get_executions_info(self):
        """
        Extrae los datos básicos de todas las ejecuciones realizadas.

        Lee el directorio de salida ('./output') y extrae los nombres de las ejecuciones,
        luego organiza la información de cada ejecución en un formato adecuado.

        Returns:
            list: Lista con los datos básicos de todas las ejecuciones.
        """
        if not os.path.exists('./output'):
            return []

        l = sorted(os.listdir('./output'), reverse=True)
        tarjetas = []

        for e in l:
            with open('./output/' + e + '/informacion.txt', 'r') as file:
                name = file.readline().split(':')[1]
                file.readline()
                timestamp = file.readline().split(': ')[1]
                date = timestamp[:10]
                hour = timestamp[11:19]

            tarjetas.append({'name': name,
                            'date': date,
                             'hour': hour,
                             'execution_unique_name': e})

        return tarjetas
