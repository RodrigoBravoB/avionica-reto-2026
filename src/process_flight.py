import csv
import math
from pathlib import Path
import matplotlib.pyplot as plt


# ==========================================
# CONFIGURACIÓN
# ==========================================

ROOT = Path(__file__).resolve().parent.parent

ARCHIVO_ENTRADA = ROOT / "flight_log.csv"
ARCHIVO_SALIDA = ROOT / "flight_processed.csv"

CARPETA_GRAFICAS = ROOT / "media" / "plots"

VENTANA = 5
FRECUENCIA_HZ = 10


# ==========================================
# LECTURA Y VALIDACIÓN DE DATOS
# ==========================================

def leer_telemetria(ruta):

    datos = []
    registros_corruptos = 0
    tiempo_anterior = -1

    with open(ruta, "r", newline="") as archivo:

        lector = csv.reader(archivo)

        encabezados = next(lector, None)

        for fila in lector:

            try:

                if len(fila) != 4:
                    raise ValueError("Número incorrecto de columnas")

                tiempo = float(fila[0])
                altitud = float(fila[1])
                aceleracion = float(fila[2])
                temperatura = float(fila[3])

                valores = [tiempo, altitud, aceleracion, temperatura]

                if not all(math.isfinite(valor) for valor in valores):
                    raise ValueError("Dato no finito")

                if tiempo <= tiempo_anterior:
                    raise ValueError("Tiempo no creciente")

                datos.append(valores)
                tiempo_anterior = tiempo

            except ValueError:

                registros_corruptos += 1

    return datos, registros_corruptos
# ==========================================
# FILTRO DE MEDIA MÓVIL
# ==========================================

def media_movil(valores, ventana):

    resultado = []
    mitad = ventana // 2

    for i in range(len(valores)):

        inicio = max(0, i - mitad)
        final = min(len(valores), i + mitad + 1)

        grupo = valores[inicio:final]

        promedio = sum(grupo) / len(grupo)

        resultado.append(promedio)

    return resultado
# ==========================================
# CÁLCULO DE VELOCIDAD
# ==========================================

def calcular_velocidad(tiempos, altitudes):

    velocidades = []

    for i in range(len(altitudes)):

        if i == 0:

            diferencia_altura = altitudes[1] - altitudes[0]
            diferencia_tiempo = tiempos[1] - tiempos[0]

        elif i == len(altitudes) - 1:

            diferencia_altura = altitudes[i] - altitudes[i - 1]
            diferencia_tiempo = tiempos[i] - tiempos[i - 1]

        else:

            diferencia_altura = altitudes[i + 1] - altitudes[i - 1]
            diferencia_tiempo = tiempos[i + 1] - tiempos[i - 1]

        velocidad = diferencia_altura / diferencia_tiempo

        velocidades.append(velocidad)

    return velocidades
# ==========================================
# DETECCIÓN DE EVENTOS
# ==========================================

def detectar_eventos(tiempos, altitudes):

    # Detectar despegue
    indice_despegue = None

    for i in range(len(altitudes)):

        if altitudes[i] > 5:
            indice_despegue = i
            break

    if indice_despegue is None:
        raise ValueError("No se detectó el despegue")

    # Detectar apogeo
    indice_apogeo = indice_despegue

    for i in range(indice_despegue, len(altitudes)):

        if altitudes[i] > altitudes[indice_apogeo]:
            indice_apogeo = i

    # Detectar aterrizaje
    indice_aterrizaje = None

    for i in range(indice_apogeo, len(altitudes) - 9):

        permanece_en_tierra = True

        for j in range(i, i + 10):

            if altitudes[j] > 2:
                permanece_en_tierra = False
                break

        if permanece_en_tierra:
            indice_aterrizaje = i
            break

    if indice_aterrizaje is None:
        raise ValueError("No se detectó el aterrizaje")

    return indice_despegue, indice_apogeo, indice_aterrizaje
# ==========================================
# GUARDAR DATOS PROCESADOS
# ==========================================

def guardar_datos(tiempos_ms, altitud_original,
                  altitud_filtrada, velocidad_original,
                  velocidad_filtrada):

    with open(ARCHIVO_SALIDA, "w", newline="") as archivo:

        escritor = csv.writer(archivo)

        escritor.writerow([
            "time_ms",
            "altitude_raw_m",
            "altitude_filtered_m",
            "velocity_raw_ms",
            "velocity_filtered_ms"
        ])

        for i in range(len(tiempos_ms)):

            escritor.writerow([
                tiempos_ms[i],
                round(altitud_original[i], 3),
                round(altitud_filtrada[i], 3),
                round(velocidad_original[i], 3),
                round(velocidad_filtrada[i], 3)
            ])
# ==========================================
# GENERACIÓN DE GRÁFICAS
# ==========================================

def generar_graficas(tiempos, altitud_original,
                     altitud_filtrada, velocidad_original,
                     velocidad_filtrada, eventos):

    indice_despegue, indice_apogeo, indice_aterrizaje = eventos

    CARPETA_GRAFICAS.mkdir(parents=True, exist_ok=True)

    # Gráfica de altitud
    plt.figure(figsize=(11, 6))

    plt.plot(
        tiempos,
        altitud_original,
        label="Altitud original",
        alpha=0.5
    )

    plt.plot(
        tiempos,
        altitud_filtrada,
        label="Altitud filtrada",
        linewidth=2
    )

    for indice, nombre in [
        (indice_despegue, "Despegue"),
        (indice_apogeo, "Apogeo"),
        (indice_aterrizaje, "Aterrizaje")
    ]:

        plt.axvline(
            tiempos[indice],
            linestyle="--",
            label=nombre
        )

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Altitud (m)")
    plt.title("Altitud durante la simulación")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(CARPETA_GRAFICAS / "altitude_vs_time.png")
    plt.close()

    # Gráfica de velocidad
    plt.figure(figsize=(11, 6))

    plt.plot(
        tiempos,
        velocidad_original,
        label="Velocidad original",
        alpha=0.5
    )

    plt.plot(
        tiempos,
        velocidad_filtrada,
        label="Velocidad filtrada",
        linewidth=2
    )

    plt.axhline(0, linestyle="--")

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Velocidad vertical (m/s)")
    plt.title("Velocidad vertical durante la simulación")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(CARPETA_GRAFICAS / "velocity_vs_time.png")
    plt.close()
# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():

    print("PROCESAMIENTO DE TELEMETRÍA")
    print("----------------------------")

    # 1. Leer y validar
    datos, corruptos = leer_telemetria(ARCHIVO_ENTRADA)

    if len(datos) < 2:
        raise ValueError("No hay suficientes registros válidos")

    print("Registros válidos:", len(datos))
    print("Registros corruptos:", corruptos)

    # 2. Separar las variables
    tiempos_ms = [registro[0] for registro in datos]
    altitudes = [registro[1] for registro in datos]

    tiempos = [tiempo / 1000 for tiempo in tiempos_ms]

    # 3. Aplicar media móvil
    altitudes_filtradas = media_movil(altitudes, VENTANA)

    # 4. Calcular velocidades
    velocidades_originales = calcular_velocidad(
        tiempos,
        altitudes
    )

    velocidades_filtradas = calcular_velocidad(
        tiempos,
        altitudes_filtradas
    )

    # 5. Detectar eventos
    eventos = detectar_eventos(
        tiempos,
        altitudes_filtradas
    )

    indice_despegue, indice_apogeo, indice_aterrizaje = eventos

    # 6. Calcular métricas
    tiempo_apogeo = tiempos[indice_apogeo]
    altitud_apogeo = altitudes_filtradas[indice_apogeo]

    velocidad_maxima = max(
        velocidades_filtradas[indice_despegue:indice_apogeo + 1]
    )

    tiempo_total = (
        tiempos[indice_aterrizaje]
        - tiempos[indice_despegue]
    )

    tiempo_descenso = (
        tiempos[indice_aterrizaje]
        - tiempos[indice_apogeo]
    )

    velocidad_media_descenso = (
        altitudes_filtradas[indice_apogeo]
        - altitudes_filtradas[indice_aterrizaje]
    ) / tiempo_descenso

    # 7. Guardar resultados
    guardar_datos(
        tiempos_ms,
        altitudes,
        altitudes_filtradas,
        velocidades_originales,
        velocidades_filtradas
    )

    generar_graficas(
        tiempos,
        altitudes,
        altitudes_filtradas,
        velocidades_originales,
        velocidades_filtradas,
        eventos
    )

    # 8. Mostrar resumen
    print("\nRESULTADOS")
    print("----------------------------")
    print("Tiempo de despegue:", round(tiempos[indice_despegue], 2), "s")
    print("Tiempo de apogeo:", round(tiempo_apogeo, 2), "s")
    print("Altitud máxima:", round(altitud_apogeo, 2), "m")
    print("Velocidad máxima de ascenso:", round(velocidad_maxima, 2), "m/s")
    print("Velocidad media de descenso:", round(velocidad_media_descenso, 2), "m/s")
    print("Tiempo total:", round(tiempo_total, 2), "s")

    print("\nArchivos generados:")
    print("flight_processed.csv")
    print("media/plots/altitude_vs_time.png")
    print("media/plots/velocity_vs_time.png")


if __name__ == "__main__":
    main()