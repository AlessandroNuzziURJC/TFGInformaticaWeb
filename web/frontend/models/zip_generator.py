import os
import shutil


class ZipGenerator:
    """
    Clase para generar un archivo ZIP con los datos de una ejecución.

    Esta clase facilita la generación de un archivo ZIP que contiene todos los datos
    generados durante una ejecución.

    Attributes:
        execution_unique_name (str): Nombre único de la ejecución.
    """

    def __init__(self, execution_unique_name):
        """
        Inicializa la instancia de ZipGenerator con el nombre único de la ejecución.

        Args:
            execution_unique_name (str): Nombre único de la ejecución.
        """
        self.execution_unique_name = execution_unique_name

    def generate(self):
        """
        Genera un archivo ZIP con todos los datos generados en una ejecución.

        Lee los archivos generados durante la ejecución, los comprime en un archivo ZIP
        y devuelve el contenido del ZIP en un diccionario.

        Returns:
            dict: Diccionario con el contenido del archivo ZIP y su nombre.
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
