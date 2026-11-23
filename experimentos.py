"""Campaña experimental de comparación de los tres algoritmos LCS.

Ejecuta procesos aislados, valida resultados y exporta mediciones y medianas."""


import csv
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

from generar_datos import generar_casos


ALGORITMOS = ["recursivo", "hirschberg", "dinamico"]
REPETICIONES = 3
TIEMPO_LIMITE = 120

CARPETA = Path(__file__).resolve().parent


def es_subsecuencia(subsecuencia, cadena):
    """Comprueba si los caracteres aparecen en orden dentro de la cadena."""

    posicion = 0

    for caracter in cadena:
        if (
            posicion < len(subsecuencia)
            and caracter == subsecuencia[posicion]
        ):
            posicion += 1

    return posicion == len(subsecuencia)


def resultado_vacio(algoritmo, longitud, repeticion, estado):
    """Construye una fila sin métricas para un fallo o una omisión."""

    return {
        "algoritmo": algoritmo,
        "longitud": longitud,
        "repeticion": repeticion,
        "estado": estado,
        "tiempo_cpu": None,
        "tiempo_real": None,
        "memoria_pico_kib": None,
        "longitud_lcs": None
    }


def ejecutar_algoritmo(algoritmo, X, Y, repeticion):

    """Ejecuta la medición en otro proceso con un límite de 120 segundos.

El tiempo real incluye el arranque del proceso y no equivale al
tiempo de CPU medido dentro del proceso auxiliar."""

    comando = [
        sys.executable,
        str(CARPETA / "medir_algoritmo.py"),
        algoritmo,
        X,
        Y
    ]

    inicio = time.perf_counter()

    try:
        proceso = subprocess.run(
            comando,
            cwd=CARPETA,
            capture_output=True,
            text=True,
            timeout=TIEMPO_LIMITE,
            check=True
        )

        datos = json.loads(proceso.stdout)

        datos["repeticion"] = repeticion
        datos["estado"] = "COMPLETADO"
        datos["tiempo_real"] = (
            time.perf_counter() - inicio
        )

        return datos

    except subprocess.TimeoutExpired:
        return resultado_vacio(
            algoritmo, len(X), repeticion, "TIMEOUT"
        )

    except subprocess.CalledProcessError as error:
        print(f"ERROR: {algoritmo}, longitud {len(X)}")
        print(error.stderr)

        return resultado_vacio(
            algoritmo, len(X), repeticion, "ERROR"
        )


def ejecutar_experimentos():

    """Ejecuta tres repeticiones por algoritmo y tamaño y exporta CSV.

La solución dinámica sirve como referencia para validar longitudes.
Tras un timeout recursivo, se omiten los tamaños recursivos mayores."""

    casos = generar_casos()
    resultados = []

    recursivo_bloqueado = False

    for longitud, X, Y in casos:

        print(f"\nLONGITUD: {longitud}")
        print("=" * 45)

        # Referencia para comprobar la longitud optima
        referencia = ejecutar_algoritmo(
            "dinamico", X, Y, 0
        )

        if referencia["estado"] != "COMPLETADO":
            raise RuntimeError(
                f"Fallo de referencia en longitud {longitud}"
            )

        longitud_optima = referencia["longitud_lcs"]

        for algoritmo in ALGORITMOS:

            for repeticion in range(1, REPETICIONES + 1):

                print(
                    f"{algoritmo} | repeticion {repeticion}",
                    flush=True
                )

                if (
                    algoritmo == "recursivo"
                    and recursivo_bloqueado
                ):
                    datos = resultado_vacio(
                        algoritmo,
                        longitud,
                        repeticion,
                        "NO_EJECUTADO"
                    )

                else:
                    datos = ejecutar_algoritmo(
                        algoritmo, X, Y, repeticion
                    )

                if datos["estado"] == "COMPLETADO":

                    resultado = datos["resultado_lcs"]

                    valido = (
                        es_subsecuencia(resultado, X)
                        and es_subsecuencia(resultado, Y)
                        and len(resultado) == longitud_optima
                    )

                    if not valido:
                        datos["estado"] = "INCORRECTO"

                if (
                    algoritmo == "recursivo"
                    and datos["estado"] in ("TIMEOUT", "ERROR")
                ):
                    recursivo_bloqueado = True

                resultados.append(datos)

                print(f"  Estado: {datos['estado']}")

                if datos["estado"] == "COMPLETADO":
                    print(
                        f"  CPU: {datos['tiempo_cpu']:.6f} s"
                    )
                    print(
                        f"  Memoria: "
                        f"{datos['memoria_pico_kib']:.3f} KiB"
                    )

    # Guardar todas las repeticiones, incluso TIMEOUT y NO_EJECUTADO.
    # Las métricas no disponibles se registran como campos vacíos.
    # Guardar resultados individuales
    columnas = [
        "algoritmo",
        "longitud",
        "repeticion",
        "estado",
        "tiempo_cpu",
        "tiempo_real",
        "memoria_pico_kib",
        "longitud_lcs"
    ]

    with open(
        CARPETA / "resultados_repeticiones.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas,
            extrasaction="ignore"
        )

        escritor.writeheader()
        escritor.writerows(resultados)

    # Excluir ejecuciones incompletas del cálculo de las medianas.
    # Calcular medianas de las ejecuciones completas
    resumen = []

    for longitud, _, _ in casos:
        for algoritmo in ALGORITMOS:

            grupo = [
                dato for dato in resultados
                if dato["longitud"] == longitud
                and dato["algoritmo"] == algoritmo
                and dato["estado"] == "COMPLETADO"
            ]

            if grupo:

                resumen.append({
                    "algoritmo": algoritmo,
                    "longitud": longitud,
                    "completadas": len(grupo),
                    "mediana_cpu": statistics.median(
                        dato["tiempo_cpu"] for dato in grupo
                    ),
                    "mediana_memoria_kib": statistics.median(
                        dato["memoria_pico_kib"] for dato in grupo
                    )
                })

    with open(
        CARPETA / "resultados_resumen.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        columnas_resumen = [
            "algoritmo",
            "longitud",
            "completadas",
            "mediana_cpu",
            "mediana_memoria_kib"
        ]

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas_resumen
        )

        escritor.writeheader()
        escritor.writerows(resumen)

    print("\nEXPERIMENTOS FINALIZADOS")
    print("Generados:")
    print(" - resultados_repeticiones.csv")
    print(" - resultados_resumen.csv")


if __name__ == "__main__":
    ejecutar_experimentos()
