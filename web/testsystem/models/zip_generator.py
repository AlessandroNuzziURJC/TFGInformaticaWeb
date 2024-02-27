import os
import shutil


class ZipGenerator:

    def __init__(self, execution_unique_name):
        self.execution_unique_name = execution_unique_name

    def generate(self):
        """
            Genera un zip con todos los datos generados en una ejecución

        Args:

        Returns:
            Devuelve un diccionario con el zip.
        """
        ruta_carpeta = os.path.join('./output/', self.execution_unique_name)
        nombre_zip = f'{self.execution_unique_name}_data.zip'
        ruta_zip = os.path.join('./output/', nombre_zip)
        shutil.make_archive(ruta_zip[:-4], 'zip', ruta_carpeta)

        content = {}

        with open(ruta_zip, 'rb') as f:
            content['file'] = f.read()

        content['nombre_zip'] = nombre_zip
        os.remove(ruta_zip)
        return content
