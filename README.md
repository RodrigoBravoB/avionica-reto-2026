# Avionica Reto 2026

## Descripción

Proyecto desarrollado para el reto de reclutamiento de la División de Aviónica de la AAIAQ, correspondiente al periodo Otoño 2026.

El proyecto consiste en el desarrollo de un sistema de adquisición y procesamiento de datos de telemetría mediante una simulación de vuelo. El sistema genera registros de diferentes etapas de una misión, permite identificar mediciones corruptas, procesa las variables registradas y presenta los resultados mediante métricas y gráficas.

## Objetivo

Desarrollar una herramienta en Python capaz de generar y procesar registros de telemetría simulada, validar la integridad de los datos, aplicar técnicas de filtrado, calcular la velocidad vertical y detectar eventos relevantes durante el vuelo.

## Ruta seleccionada

**Ruta 1: Telemetría y adquisición de datos.**

## Tecnologías y herramientas

- Python 3
- Matplotlib
- Archivos CSV
- Git
- GitHub
- LaTeX y MiKTeX para la documentación técnica

## Estructura del proyecto

```text
avionica-reto-2026/
├── src/
│   ├── generate_flight.py
│   └── process_flight.py
├── docs/
│   ├── reporte.tex
│   └── reporte.pdf
├── media/
│   └── plots/
│       ├── altitude_vs_time.png
│       ├── velocity_vs_time.png
│       ├── comparison_altitude.png
│       └── comparison_velocity.png
├── flight_log.csv
├── flight_processed.csv
├── README.md
└── .gitignore
```

## Funcionamiento

El proyecto se divide en dos programas principales:

### 1. Generación de telemetría

El archivo `generate_flight.py` simula las diferentes etapas del vuelo y genera un archivo CSV con las mediciones registradas.

Las variables generadas son:

- Tiempo de muestreo.
- Altitud.
- Aceleración vertical.
- Temperatura.

La simulación incorpora ruido en las mediciones e incluye registros corruptos para comprobar la capacidad de validación del sistema.

### 2. Procesamiento de datos

El archivo `process_flight.py` realiza la lectura y validación del archivo generado. Posteriormente, aplica un filtro de media móvil, calcula la velocidad vertical mediante diferencias finitas y detecta los principales eventos del vuelo.

También obtiene métricas de desempeño y genera representaciones gráficas para analizar el comportamiento de las variables.

## Resultados generados

- `flight_log.csv`: registro original de telemetría simulada.
- `flight_processed.csv`: datos validados y procesados.
- `altitude_vs_time.png`: comparación de altitud original y filtrada.
- `velocity_vs_time.png`: comparación de velocidad vertical original y filtrada.
- `comparison_altitude.png`: comparación del efecto de diferentes ventanas de filtrado sobre la altitud.
- `comparison_velocity.png`: comparación del efecto de diferentes ventanas de filtrado sobre la velocidad.

## Instalación y ejecución

Se requiere Python 3 y la biblioteca Matplotlib.

Instalar la dependencia con:

```bash
python -m pip install matplotlib
```

Desde el directorio raíz del proyecto, ejecutar primero el generador:

```bash
python src/generate_flight.py
```

Después, ejecutar el programa de procesamiento:

```bash
python src/process_flight.py
```

Los archivos CSV y las gráficas se generan en las ubicaciones definidas por los programas.

## Autoría

**Rodrigo Bravo**

Proyecto desarrollado individualmente como parte del reto de reclutamiento de la División de Aviónica AAIAQ, Otoño 2026.