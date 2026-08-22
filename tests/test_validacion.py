# tests/test_validacion.py
#? Pruebas unitarias para las funciones de validación.
#? Verificamos que validar_columnas, detectar_duplicados y contar_nulos funcionen correctamente.

import pytest
import pandas as pd
import sys
import os

# Agregar la raíz del proyecto al path para importar el módulo principal.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from taller_3_g6 import validar_columnas, detectar_duplicados, contar_nulos

def test_validar_columnas_exitoso(sample_df):
    """Prueba que valida correctamente columnas presentes."""
    #? Caso feliz: todas las columnas requeridas existen.
    columnas = ['id_estudiante', 'nombre', 'puntaje']
    resultado = validar_columnas(sample_df, columnas, 'TestDF')
    assert resultado is True

def test_validar_columnas_faltante(sample_df):
    """Prueba que lanza error si falta una columna."""
    #? Caso de error: columna 'edad' no existe en el DataFrame.
    #? La función debe lanzar ValueError con un mensaje descriptivo.
    columnas = ['id_estudiante', 'nombre', 'puntaje', 'edad']
    with pytest.raises(ValueError, match="TestDF sin columnas: \\['edad'\\]"):
        validar_columnas(sample_df, columnas, 'TestDF')

def test_detectar_duplicados_con_duplicados():
    """Prueba que detecta duplicados en el subset."""
    #? DataFrame con IDs repetidos: A y B aparecen dos veces.
    df = pd.DataFrame({
        'id': ['A', 'B', 'A', 'C', 'B'],
        'valor': [1, 2, 3, 4, 5]
    })
    dupes = detectar_duplicados(df, subset=['id'], nombre_df='Test')
    #? Duplicados = registros que tienen un valor repetido en 'id'.
    #? A aparece en filas 0 y 2; B en filas 1 y 4 → 4 registros duplicados.
    assert len(dupes) == 4

def test_detectar_duplicados_sin_duplicados(sample_df):
    """Prueba que no detecta duplicados cuando no existen."""
    #? Todos los id_estudiante son únicos en el fixture sample_df.
    dupes = detectar_duplicados(sample_df, subset=['id_estudiante'], nombre_df='Test')
    assert len(dupes) == 0

def test_contar_nulos(sample_df):
    """Prueba que cuenta correctamente los valores nulos."""
    #? En sample_df, solo hay un nulo en la columna 'puntaje' (fila E002).
    nulos = contar_nulos(sample_df, 'puntaje', 'Test')
    assert nulos == 1

def test_contar_nulos_sin_nulos():
    """Prueba que retorna 0 si no hay nulos."""
    #? DataFrame sin valores nulos.
    df = pd.DataFrame({'col': [1, 2, 3]})
    nulos = contar_nulos(df, 'col', 'Test')
    assert nulos == 0
