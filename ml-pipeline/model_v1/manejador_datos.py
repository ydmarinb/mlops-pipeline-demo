import os
import shutil
from typing import NoReturn

def copiar_ultimo_archivo_en_carpeta_actual() -> NoReturn:
    """
    Encuentra el archivo más recientemente modificado en el directorio 'data_pipeline/clean_data'
    y copia este archivo al directorio de ejecución actual de la función.

    :return: None
    """
    # Ruta al directorio de donde se buscarán los archivos
    directorio_objetivo: str = '../../data-pipeline/clean_data'
    
    # Lista de archivos en el directorio, ignorando subdirectorios
    archivos: list[str] = [archivo for archivo in os.listdir(directorio_objetivo) 
                           if os.path.isfile(os.path.join(directorio_objetivo, archivo))]
    
    # Si no hay archivos en la carpeta, terminar la función
    if not archivos:
        print("No hay archivos en la carpeta objetivo.")
        return

    # Ruta completa al archivo más reciente
    ultimo_archivo: str = max([os.path.join(directorio_objetivo, archivo) for archivo in archivos], 
                              key=os.path.getmtime)
    
    # Ruta al directorio de ejecución actual
    directorio_actual: str = os.getcwd()
    
    # Crear una copia del último archivo en el directorio actual
    shutil.copy(ultimo_archivo, directorio_actual)
    print(f"Archivo copiado: {os.path.basename(ultimo_archivo)} al directorio {directorio_actual}")
    
    
import os

def obtener_nombre_csv_unico(directorio: str) -> str:
    """
    Busca en el directorio dado y retorna el nombre del único archivo CSV encontrado.
    
    :param directorio: La ruta del directorio en el que buscar el archivo CSV.
    :return: El nombre del archivo CSV único en el directorio.
    :raises ValueError: Si no hay archivos CSV o hay más de uno en el directorio.
    """
    # Lista de todos los archivos CSV en el directorio
    archivos_csv = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.csv')]
    
    # Verificar que solo hay un archivo CSV
    if len(archivos_csv) == 1:
        return archivos_csv[0]
    elif len(archivos_csv) == 0:
        raise ValueError("No se encontraron archivos CSV en el directorio.")
    else:
        raise ValueError("Hay más de un archivo CSV en el directorio.")







