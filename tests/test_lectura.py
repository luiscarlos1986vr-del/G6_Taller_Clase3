# tests/test_lectura.py
#? Pruebas unitarias para la función leer_archivo_seguro.
#? Verificamos que lea correctamente CSV, Excel y JSON, y que maneje errores.

import pytest
import pandas as pd
from pathlib import Path
import sys
import os

# Agregar la raíz del proyecto al path para importar el módulo principal.
#? Esto permite importar funciones de taller_3_g6.py sin tener que instalar el paquete.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from taller_3_g6 import leer_archivo_seguro

def test_leer_csv(temp_csv):
    """Prueba que lea correctamente un archivo CSV."""
    #? Caso feliz: archivo CSV bien formado.
    df = leer_archivo_seguro(temp_csv, tipo='csv')
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 3)  # 3 filas x 3 columnas
    assert list(df.columns) == ['id', 'nombre', 'puntaje']

def test_leer_excel(temp_excel):
    """Prueba que lea correctamente un archivo Excel."""
    #? Caso feliz: archivo Excel con engine openpyxl.
    df = leer_archivo_seguro(temp_excel, tipo='excel', engine='openpyxl')
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 3)
    assert list(df.columns) == ['id', 'nombre', 'puntaje']

def test_leer_json(tmp_path):
    """Prueba que lea correctamente un archivo JSON."""
    #? Caso feliz: archivo JSON con orientación de registros.
    json_file = tmp_path / "test.json"
    import json
    data = [{"id": "E001", "nombre": "Ana", "puntaje": 95}]
    json_file.write_text(json.dumps(data))
    
    df = leer_archivo_seguro(json_file, tipo='json')
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 3)

def test_leer_tipo_no_soportado():
    """Prueba que lanza error para tipo no soportado."""
    #? Verificamos que la función falle temprano con un tipo inválido.
    with pytest.raises(ValueError, match="Tipo no soportado: parquet"):
        leer_archivo_seguro(Path("fake.parquet"), tipo='parquet')

def test_leer_csv_con_dtypes(temp_csv):
    """Prueba que preserve tipos de datos especificados (ej. IDs como str)."""
    #? Este caso es crítico: si los IDs se convierten a número, se pierden ceros.
    #? Forzamos dtype str para preservar el formato original.
    df = leer_archivo_seguro(temp_csv, tipo='csv', dtype={'id': str})
    assert df['id'].dtype == 'object'  # str se almacena como object en pandas
    assert df['id'].iloc[0] == 'E001'
