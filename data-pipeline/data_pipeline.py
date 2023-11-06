import pandas as pd
import numpy as np
from data_standardization import arreglar_direccion
from data_evaluation import Caracter
from datetime import datetime
import yaml
import os
from datetime import datetime

def leer_parametros_yaml(archivo_yaml: str) -> dict:
    """
    Lee los parámetros de un archivo YAML y los retorna.
    
    Args:
    archivo_yaml (str): La ruta al archivo YAML que contiene los parámetros.
    
    Returns:
    dict: Un diccionario con los parámetros leídos.
    """
    with open(archivo_yaml, 'r') as stream:
        try:
            parametros = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
    return parametros

def validar_archivos_nuevos(carpeta: str, archivo_lista: str) -> list:
    """
    Valida qué archivos en la carpeta especificada no están listados en el archivo de texto.
    
    Args:
    carpeta (str): Ruta a la carpeta donde se buscarán los archivos.
    archivo_lista (str): Ruta al archivo de texto que contiene la lista de archivos procesados.
    
    Returns:
    list: Lista con los nombres de los archivos que no están en el archivo de texto.
    """
    with open(archivo_lista, 'r') as lista:
        archivos_procesados = set(lista.read().splitlines()).union({'historial.txt', 'feature_data.csv'})
    archivos_en_carpeta = set(os.listdir(carpeta))
    return list(archivos_en_carpeta - archivos_procesados)

def agregar_a_historial(nombre_archivo: str, archivo_historial: str = 'raw_data/historial.txt') -> None:
    """
    Agrega el nombre de un archivo procesado a un archivo de historial.
    
    Args:
    nombre_archivo (str): Nombre del archivo que ha sido procesado.
    archivo_historial (str): Ruta al archivo de historial donde se registrará el nombre del archivo.
    """
    with open(archivo_historial, 'a') as historial:
        historial.write(nombre_archivo + '\n')

def procesar_archivos(archivos_no_procesados: list, parametros: dict) -> None:
    """
    Procesa los archivos especificados aplicando una serie de transformaciones estandarizadas.
    
    Args:
    archivos_no_procesados (list): Lista de archivos que no han sido procesados aún.
    parametros (dict): Diccionario con los parámetros necesarios para la estandarización.
    """
    for archivo in archivos_no_procesados:
        df = pd.read_csv(f'raw_data/{archivo}')
        direccion = Caracter(df['direccion'])
        consistencia_direccion_antes = direccion.evaluacion_consistencia(
            estandar=parametros['estandar_direccion'],
            diccionario_dominios=parametros['diccionario_dominios_direccion'],
            tildes=False,
            numeros=True,
            mayusculas=True,
            minusculas=False,
            categorias_teoricas=parametros['categorias_teoricas_direccion'],
            letras=True)

        direcciones_buenas = [arreglar_direccion(str(i), parametros['categorias_esperada']) for i in df['direccion']]
        
        df['direccion'] = direcciones_buenas
        direccion = Caracter(df['direccion'])
        consistencia_direccion_despues = direccion.evaluacion_consistencia(
            estandar=parametros['estandar_direccion'],
            diccionario_dominios=parametros['diccionario_dominios_direccion'],
            tildes=False,
            numeros=True,
            mayusculas=True,
            minusculas=False,
            categorias_teoricas=parametros['categorias_teoricas_direccion'],
            letras=True)

        agregar_a_historial(archivo)
        if (parametros['cosistencia_minima_esperada'] > consistencia_direccion_despues) or (consistencia_direccion_despues < consistencia_direccion_antes):
            file_path = f'clean_data/baja_calidad_{archivo}'
            open(file_path, 'w').close()
        else:
            df_features = pd.read_csv('raw_data/feature_data.csv')
            df_features = df_features.set_index('id_usuario').join(df.set_index('id_usuario'))
            df_features.reset_index().to_csv(f'clean_data/data_{str(datetime.now())}.csv', index=False)

if __name__ == "__main__":
    parametros = leer_parametros_yaml('metadatos.yaml')
    archivos_no_procesados = validar_archivos_nuevos('raw_data', 'raw_data/historial.txt')
    procesar_archivos(archivos_no_procesados, parametros)
 
        
