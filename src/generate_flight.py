import csv
import random

# ==========================================
# CONFIGURACIÓN DE LA SIMULACIÓN
# ==========================================

FRECUENCIA_HZ = 10
DT = 1 / FRECUENCIA_HZ
INTERVALO_MS = 100

GRAVEDAD = 9.81
ACELERACION_NETA = 60.0

ALTITUD_INICIAL = 0.0
TEMPERATURA_INICIAL = 25.0
TASA_TEMPERATURA = 0.0065

ARCHIVO_SALIDA = "flight_log.csv"


# ==========================================
# FUNCIÓN PARA GENERAR UNA MEDICIÓN
# ==========================================

def crear_medicion(tiempo_ms, altitud, aceleracion):

    # Ruido aleatorio de los sensores
    altitud_medida = altitud + random.gauss(0, 0.5)

    # Evitamos altitudes negativas por el ruido
    if altitud_medida < 0:
        altitud_medida = 0

    temperatura = (
        TEMPERATURA_INICIAL
        - TASA_TEMPERATURA * altitud
    )

    temperatura_medida = temperatura + random.gauss(0, 0.2)

    return [
        tiempo_ms,
        round(altitud_medida, 2),
        round(aceleracion, 2),
        round(temperatura_medida, 2)
    ]


# ==========================================
# GENERACIÓN DE DATOS
# ==========================================

datos = []

tiempo_ms = 0
altitud = ALTITUD_INICIAL
velocidad = 0.0


# FASE 1: PREPARACIÓN (2 segundos)

for i in range(21):

    medicion = crear_medicion(
        tiempo_ms,
        altitud,
        GRAVEDAD
    )

    datos.append(medicion)
    tiempo_ms += INTERVALO_MS


# FASE 2: ACELERACIÓN (1.5 segundos)

numero_pasos = int(1.5 * FRECUENCIA_HZ)

for i in range(numero_pasos):

    altitud += (
        velocidad * DT
        + 0.5 * ACELERACION_NETA * DT**2
    )

    velocidad += ACELERACION_NETA * DT

    aceleracion_sensor = ACELERACION_NETA + GRAVEDAD

    medicion = crear_medicion(
        tiempo_ms,
        altitud,
        aceleracion_sensor
    )

    datos.append(medicion)
    tiempo_ms += INTERVALO_MS


# FASE 3: ASCENSO BALÍSTICO HASTA EL APOGEO

while velocidad > 0:

    velocidad_nueva = velocidad - GRAVEDAD * DT

    if velocidad_nueva <= 0:

        # Calculamos el apogeo dentro del último intervalo
        altitud += velocidad**2 / (2 * GRAVEDAD)
        velocidad = 0

    else:

        altitud += (
            velocidad * DT
            - 0.5 * GRAVEDAD * DT**2
        )

        velocidad = velocidad_nueva

    # En caída balística, el acelerómetro ideal
    # registra aproximadamente 0 m/s².
    medicion = crear_medicion(
        tiempo_ms,
        altitud,
        0.0
    )

    datos.append(medicion)
    tiempo_ms += INTERVALO_MS
altitud_apogeo = altitud

# FASE 4: DESCENSO SIMULADO (6 m/s)

VELOCIDAD_DESCENSO = 6.0

while altitud > 0:

    altitud -= VELOCIDAD_DESCENSO * DT

    if altitud < 0:
        altitud = 0

    medicion = crear_medicion(
        tiempo_ms,
        altitud,
        GRAVEDAD
    )

    datos.append(medicion)
    tiempo_ms += INTERVALO_MS


# FASE 5: PERMANENCIA EN TIERRA (3 segundos)

numero_pasos = int(3 * FRECUENCIA_HZ)

for i in range(numero_pasos):

    medicion = crear_medicion(
        tiempo_ms,
        0,
        GRAVEDAD
    )

    datos.append(medicion)
    tiempo_ms += INTERVALO_MS


# ==========================================
# ESCRITURA DEL ARCHIVO CSV
# ==========================================

with open(ARCHIVO_SALIDA, "w", newline="") as archivo:

    escritor = csv.writer(archivo)

    escritor.writerow([
        "time_ms",
        "altitude_m",
        "accel_z_ms2",
        "temp_c"
    ])

    for i, registro in enumerate(datos):

        escritor.writerow(registro)

        # Insertamos tres registros corruptos de prueba

        if i == 100:
            escritor.writerow([
                registro[0], "", registro[2], registro[3]
            ])

        elif i == 300:
            escritor.writerow([
                registro[0], "ERROR", registro[2], registro[3]
            ])

        elif i == 500:
            escritor.writerow([
                registro[0], registro[1], registro[2]
            ])


# ==========================================
# RESUMEN DE LA SIMULACIÓN
# ==========================================

print("SIMULACIÓN TERMINADA")
print("-------------------------")
print("Archivo generado:", ARCHIVO_SALIDA)
print("Registros válidos:", len(datos))
print("Registros corruptos insertados: 3")
print("Frecuencia de muestreo:", FRECUENCIA_HZ, "Hz")
print("Intervalo:", INTERVALO_MS, "ms")
print("Altitud máxima teórica:", round(altitud_apogeo, 2), "m")