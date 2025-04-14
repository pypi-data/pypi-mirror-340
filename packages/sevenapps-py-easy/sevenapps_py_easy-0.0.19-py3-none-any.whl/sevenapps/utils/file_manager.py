import json
import os
import sys
from datetime import datetime


def check_if_exist_file_in_folder(file_path):
    """
    Comprueba si un archivo existe en una carpeta dada. Pasa la ruta del archivo y devuelve True si existe o False en caso contrario.

    Parámetros:
    file_path (str): Ruta del archivo a comprobar.

    Retorna:
    bool: True si el archivo existe, False en caso contrario.
    """

    folder_path, file_name = os.path.split(file_path)

    if os.path.exists(folder_path):
        folder_files = os.listdir(folder_path)

        if file_name in folder_files:
            return True
        else:
            return False
    else:
        return False


def remove_file(file_path):
    """
    Elimina un archivo en una carpeta dada. Pasa la ruta del archivo como par metro y devuelve True si se ha eliminado correctamente o False en caso contrario.

    Parámetros:
    file_path (str): Ruta del archivo a eliminar.

    Retorna:
    bool: True si el archivo se ha eliminado correctamente, False en caso contrario.
    """
    folder_path, file_name = os.path.split(file_path)

    if os.path.exists(folder_path):
        folder_files = os.listdir(folder_path)

        if file_name in folder_files:
            file_to_remove = os.path.join(folder_path, file_name)
            os.remove(file_to_remove)
            return True
        else:
            return False
    else:
        return False


def read_json_file(path):
    """
    Lee un archivo JSON y devuelve su contenido como un diccionario.

    Parámetros:
    path (str): Ruta del archivo JSON a leer.

    Retorna:
    dict: Contenido del archivo JSON como un diccionario.
    """
    f = open(path)

    config = json.load(f)

    f.close()

    return config


def rename_file(path, new_name):
    """
    Renombra un archivo en una ruta dada.

    Parámetros:
    path (str): Ruta del archivo a renombrar.
    new_name (str): Nuevo nombre para el archivo.

    Retorna:
    None
    """
    if os.path.exists(path):
        folder_path, file_name = os.path.split(path)
        new_path = os.path.join(folder_path, new_name)
        os.rename(path, new_path)
        print(f"[ARCHIVO RENOMBRADO]: El archivo {file_name} ha sido renombrado como {new_name}.")
    else:
        print("[ERROR]: El archivo especificado no existe")


def generate_file_name_with_date(file_name):
    """
    Genera un nombre de archivo con la fecha y hora actual anexadas.

    Parámetros:
    file_name (str): El nombre base del archivo.

    Retorna:
    str: El nombre del archivo anexado con la fecha y hora actual en el formato 'YYYY_MM_DD_HH_MM_SS'.
    """

    return f"{file_name}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

def read_bash_input_parameters():
    """
    Lee los parámetros de entrada desde la terminal y devuelve el primer parámetro en minúsculas.
    Si no se proporciona parámetro, devuelve la cadena "no_parameter".

    Retorna:
    str: El primer parámetro en minúsculas o "no_parameter" si no se proporciona parámetro.
    """
    if len(sys.argv) > 1:
        return sys.argv[1].lower()

    else:
        return "no_parameter"

