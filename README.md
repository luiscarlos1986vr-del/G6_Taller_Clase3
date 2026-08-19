# Taller Práctico - Flujo Analítico Reproducible

**Integrantes:** Mayra Sánchez, Josías Piña, Luis Valencia.
**Fecha:** 18 de Agosto 2026
**Repositorio:** [G6_Taller_Clase3](https://github.com/luiscarlos1986vr-del/G6_Taller_Clase3)

---

## 📌 Propósito del proyecto

Diseñar un flujo analítico reproducible que consolide las entregas de proyectos de dos campus (Matriz y Extensión) y las cruce con el catálogo maestro de estudiantes de la institución. El proceso incluye:

- Integración estructural (concatenación) de los archivos de entregas.
- Integración relacional (merge) con el catálogo de estudiantes.
- Limpieza, validación y auditoría de la calidad de los datos.
- Generación de indicadores de calidad y resúmenes analíticos.
- Exportación en múltiples formatos (CSV, JSON, Excel).

---

## 🗂️ Estructura del proyecto

```
G6_Taller_Clase3/
├── data/
│   ├── raw/                     # Datos fuente (no versionados)
│   │   ├── estudiantes_master.xlsx
│   │   ├── entregas_campus_matriz.csv
│   │   └── entregas_campus_extension.csv
│   └── processed/               # Salidas generadas (se crean al ejecutar)
│       ├── dataset_consolidado_final_YYYYMMDD.*
│       ├── resumen_analitico_YYYYMMDD.*
│       ├── indicadores_calidad_YYYYMMDD.csv
│       └── huerfanos_YYYYMMDD.csv (si existen)
├── Taller_3_G6.ipynb            # Script principal
├── requirements.txt             # Dependencias
├── .gitignore                   # Archivos y carpetas a ignorar
└── README.md                    # Este archivo
```

> **Nota:** Los archivos en `data/raw/` **no se suben al repositorio** (están en `.gitignore`). Cada usuario debe colocar allí los datos originales antes de ejecutar el script.

---

## ⚙️ Requisitos y dependencias

- Python 3.12 o superior
- Las librerías se listan en `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Contenido de `requirements.txt`

```
pandas==2.2.2
numpy==2.2.2
openpyxl==3.1.5
```

---

## 🚀 Ejecución del flujo

### Opción 1: Script Python (recomendado para producción)

```bash
python Taller_3_G6.py
```

### Opción 2: Notebook Jupyter/Colab

Abre el archivo `Taller_3_G6.ipynb` en Google Colab o en Jupyter y ejecuta las celdas en orden.

**Para Colab:**
- Monta Google Drive y copia los datos a `data/raw/` o súbelos manualmente.
- El script creará automáticamente las carpetas necesarias.

---

## 📊 Salidas generadas

Todos los archivos se guardan en `data/processed/` con un sufijo de fecha (YYYYMMDD):

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `dataset_consolidado_final_*` | CSV, JSON, Excel | Dataset completo con entregas + datos de estudiantes. |
| `resumen_analitico_*` | CSV, JSON, Excel | Promedio, conteo y desviación por estudiante y campus. |
| `indicadores_calidad_*` | CSV | Métricas de calidad del proceso. |
| `huerfanos_*` (si existen) | CSV | Entregas sin correspondencia en el catálogo. |

### 📈 Indicadores de calidad incluidos

- Archivos procesados
- Registros leídos por fuente (catálogo, matriz, extensión)
- Registros consolidados e integrados
- Duplicados eliminados
- Claves sin correspondencia (huérfanos)
- Valores nulos en puntaje
- Distribución de estados de entrega (Aprobado, Revisión, Pendiente)
- Dimensiones finales del dataset

---

## 🔁 Estrategia de reproducibilidad

1. **Entorno virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

2. **Dependencias fijas** en `requirements.txt`.

3. **Rutas relativas** con `pathlib` para que el código funcione en cualquier máquina.

4. **Control de versiones con Git**:
   - `.gitignore` excluye `data/raw/`, `__pycache__/`, `.venv/`, `*.pyc`, etc.
   - Commits con mensajes claros y frecuentes.

5. **Documentación** del flujo dentro del script (comentarios) y en este README.

6. **Operaciones deterministas**: sin aleatoriedad, todas las salidas son reproducibles.

---

## 📝 Notas adicionales

- El script valida automáticamente la presencia de columnas críticas y detiene la ejecución si falta alguna.
- Los huérfanos se exportan para revisión manual, pero no se eliminan del dataset final (se conservan con datos nulos del catálogo).
- Si se detectan estados inconsistentes (ej. "Pendiente" con puntaje), se muestra una advertencia en consola.

---

## 📧 Contacto

Para dudas o sugerencias, abrir un *issue* en el repositorio o contactar a los integrantes del equipo.

---

**¡Flujo analítico reproducible listo para usar!** 🚀
