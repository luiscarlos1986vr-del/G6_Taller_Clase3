# Taller 3 — Flujo Analítico Reproducible (v2.0)

**Integrantes:** Mayra Sánchez, Josías Piña, Luis Valencia
**Repositorio:** [G6_Taller_Clase3 — rama `Luis`](https://github.com/luiscarlos1986vr-del/G6_Taller_Clase3/tree/Luis)

---

## Propósito

Transformar un proceso manual de consolidación de datos en un flujo analítico reproducible que:

- Consolida las entregas de dos campus (Matriz y Extensión) mediante concatenación.
- Las cruza con el catálogo maestro de estudiantes mediante `merge` relacional.
- Valida, limpia y audita la calidad de los datos.
- Calcula indicadores de completitud, consistencia y unicidad.
- Exporta resultados en CSV, JSON y Excel con sello de fecha.

---

## Estructura del proyecto

```
G6_Taller_Clase3/
├── .github/workflows/python-app.yml   # CI: flake8 + pytest
├── data/
│   ├── raw/                           # Copia de los insumos (se crea al ejecutar)
│   └── processed/                     # Salidas generadas
├── logs/
│   └── pipeline.log                   # Registro de ejecución (logging)
├── tests/
│   ├── conftest.py                    # Fixtures de pytest
│   ├── test_lectura.py                # Pruebas de leer_archivo_seguro
│   └── test_validacion.py             # Pruebas de validación
├── config.json                        # Parámetros centralizados del pipeline
├── estudiantes_master.xlsx            # Catálogo maestro (fuente)
├── entregas_campus_matriz.csv         # Entregas campus Matriz (fuente)
├── entregas_campus_extension.csv      # Entregas campus Extensión (fuente)
├── Taller_3_G6.ipynb                  # Notebook interactivo
├── taller_3_g6.py                     # Script ejecutable
├── requirements.txt
├── .gitignore
└── README.md
```

Los archivos fuente viven en la raíz; el script crea `data/raw/`, `data/processed/` y `logs/`, y copia los insumos a `data/raw/` para separar el dato intocable del generado.

---

## Configuración externa (`config.json`)

Todos los parámetros están centralizados; no hay valores hardcodeados en el script.

| Clave | Contenido |
|---|---|
| `rutas` | `data/raw`, `data/processed`, `logs` |
| `archivos_fuente` | catálogo, entregas matriz, entregas extensión |
| `columnas_requeridas` | columnas obligatorias de catálogo y entregas |
| `formatos_exportacion` | `csv`, `json`, `xlsx` |
| `validaciones` | puntaje 0–100, estados `Aprobado`/`Revisión`/`Pendiente` |
| `logging` | nivel `INFO`, archivo `logs/pipeline.log`, formato |

Para adaptar el flujo a otro entorno basta editar `config.json`.

---

## Requisitos

- Python 3.10 o superior (la CI ejecuta con 3.10).
- Dependencias en `requirements.txt`: `pandas==2.2.2`, `numpy==2.2.2`, `openpyxl==3.1.5`, `jupyter`.

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

---

## Ejecución

```bash
python taller_3_g6.py          # script (recomendado)
pytest tests/                  # pruebas con pytest
```

O abre `Taller_3_G6.ipynb` en Jupyter/Colab y ejecuta las celdas en orden (sube también los `.csv`, el `.xlsx` y `config.json`).

---

## Etapas del pipeline

1. **1.1 Entorno** — logging a consola y a `logs/pipeline.log`, carga de `config.json`.
2. **1.2 Arquitectura de carpetas** — creación de `data/raw` y `data/processed`.
3. **1.3 Funciones reutilizables** — `leer_archivo_seguro`, `validar_columnas`, `detectar_duplicados`, `contar_nulos`.
4. **1.4 Pruebas internas** — 8 asserts que detienen el pipeline si fallan, además de la suite `tests/` para pytest.
5. **2.1 Lectura** — IDs forzados a `str`, validación de columnas requeridas, deduplicación del catálogo.
6. **2.2 Concat** — columna `campus` añadida antes de unir Matriz + Extensión.
7. **2.3 Merge** — `how='left'`, `validate='many_to_one'`, `indicator=True`; huérfanos exportados.
8. **2.4 Validaciones** — nulos en puntaje e inconsistencias estado/puntaje.
9. **2.5–2.6 Análisis** — descriptivos, promedios por campus/materia/tipo, top y bottom 5, resumen por estudiante.
10. **2.7 Indicadores de calidad** — completitud, consistencia y unicidad.
11. **2.8 Exportación** — CSV, JSON y XLSX con sufijo `YYYYMMDD`.
12. **2.9–3.0 Reproducibilidad y reflexión final.**

---

## Salidas generadas (`data/processed/`)

| Archivo | Formatos | Descripción |
|---|---|---|
| `dataset_integrado_YYYYMMDD.*` | CSV, JSON, XLSX | Entregas + datos del catálogo |
| `resumen_estudiantes_YYYYMMDD.*` | CSV, JSON, XLSX | Promedio, conteo y desviación por estudiante y campus |
| `indicadores_calidad_YYYYMMDD.csv` | CSV | Métricas de calidad del proceso |
| `huerfanos_YYYYMMDD.csv` | CSV | Entregas sin correspondencia en el catálogo (si existen) |

### Indicadores incluidos

- Básicos: archivos procesados, registros por fuente, consolidados, integrados, duplicados eliminados, huérfanos, nulos en puntaje, dimensiones de salida, archivos generados (verificados en disco).
- Completitud: % no nulos por columna y global.
- Consistencia: puntajes fuera de rango, estados inválidos, `Pendiente` con puntaje, `Revisión` sin puntaje, y sus porcentajes.
- Unicidad: únicos, duplicados y % para `id_entrega` e `id_estudiante`.

---

## Integración continua

`.github/workflows/python-app.yml` se ejecuta en cada push y pull request a la rama `Luis`: instala dependencias, corre `flake8` (errores críticos + reporte informativo) y `pytest tests/`.

---

## Estrategia de reproducibilidad

1. Entorno virtual aislado y dependencias fijadas por versión.
2. Parámetros externos en `config.json` en lugar de valores hardcodeados.
3. Rutas relativas con `pathlib` → portable entre máquinas y Colab.
4. Logging persistente en `logs/pipeline.log` en lugar de `print`.
5. Pruebas automatizadas (internas y con pytest) que fallan temprano.
6. Operaciones deterministas; los timestamps solo nombran archivos.
7. Control de versiones con Git y CI en GitHub Actions.
