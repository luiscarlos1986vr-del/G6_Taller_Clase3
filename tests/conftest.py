# tests/conftest.py
#? Configuración compartida para todas las pruebas con pytest.
#? Los fixtures proporcionan datos y archivos temporales reutilizables.

import pytest
import pandas as pd
from pathlib import Path
import tempfile

@pytest.fixture
def sample_df():
    """DataFrame de ejemplo para pruebas de validación."""
    #? DataFrame con datos típicos del dominio: IDs, nombres, puntajes y estados.
    #? Incluye un valor nulo intencional para probar conteo de nulos.
    return pd.DataFrame({
        'id_estudiante': ['E001', 'E002', 'E003', 'E004'],
        'nombre': ['Ana', 'Luis', 'Carlos', 'Maria'],
        'puntaje': [95, None, 88, 92],
        'estado': ['Aprobado', 'Pendiente', 'Revisión', 'Aprobado']
    })

@pytest.fixture
def temp_csv():
    """Crea un archivo CSV temporal con datos de prueba."""
    #? Usamos tempfile.NamedTemporaryFile con modo 'w+' para asegurar escritura.
    #? Eliminamos el parámetro 'delete=False' para que se limpie automáticamente.
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write("id,nombre,puntaje\n")
        f.write("E001,Ana,95\n")
        f.write("E002,Luis,88\n")
        f.write("E003,Carlos,92\n")
        f.flush()  # Asegura que los datos se escriban en el disco
        yield Path(f.name)
    # Limpieza después de la prueba
    Path(f.name).unlink(missing_ok=True)

@pytest.fixture
def temp_excel():
    """Crea un archivo Excel temporal con datos de prueba."""
    #? Similar a temp_csv pero para formato Excel.
    #? Requiere openpyxl, que ya está en requirements.txt.
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        df = pd.DataFrame({
            'id': ['E001', 'E002', 'E003'],
            'nombre': ['Ana', 'Luis', 'Carlos'],
            'puntaje': [95, 88, 92]
        })
        df.to_excel(f.name, index=False, engine='openpyxl')
        yield Path(f.name)
    # Limpieza después de la prueba.
    Path(f.name).unlink(missing_ok=True)
