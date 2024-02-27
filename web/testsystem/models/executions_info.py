import os


class ExecutionsInfo:

    def __init__(self) -> None:
        pass

    def get_executions_info(self):
        """
            Extrae los datos basicos de todas las ejecuciones realizadas.

        Args:

        Returns:
            Devuelve una lista con todas las ejecuciones.
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
