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
            name = e[22:].replace('__', ' ').title()
            if len(name) > 17:
                name = name[:17] + '...'
            aux = e[:10].split('-')
            date = f"{aux[2]}-{aux[1]}-{aux[0]}"
            hour = e[12:20]

            tarjetas.append({'name': name,
                            'date': date,
                             'hour': hour,
                             'execution_unique_name': e})

        return tarjetas
