"""Medición independiente del tiempo de CPU y del pico de memoria de LCS.

Se ejecuta como proceso auxiliar desde experimentos.py y devuelve JSON."""


import sys
import json
import time
import tracemalloc

from recursivo import lcs_recursivo
from hirschberg import hirschberg
from dinamico import lcs_dinamico


def ejecutar(algoritmo, X, Y):

    """Selecciona y ejecuta una de las tres implementaciones de LCS."""

    if algoritmo == "recursivo":
        return lcs_recursivo(
            X, Y, len(X), len(Y)
        )

    elif algoritmo == "hirschberg":
        return hirschberg(X, Y)

    elif algoritmo == "dinamico":
        return lcs_dinamico(X, Y)

    else:
        raise ValueError("Algoritmo desconocido")


def medir(algoritmo, X, Y):

    # La recursión directa se mide una vez para evitar multiplicar
    # un coste que puede crecer exponencialmente.
    # Repeticiones internas solo para algoritmos
    # eficientes y cadenas pequeñas
    
    # Medir tiempo CPU sin tracemalloc.
    # Los algoritmos rapidos se repiten para mejorar
    # la precision de las mediciones.

    """Mide CPU y memoria en ejecuciones separadas.

Para las entradas pequeñas de los algoritmos eficientes, promedia
varias ejecuciones para reducir el error de resolución del reloj.
La memoria se mide aparte con tracemalloc y se expresa en KiB."""

    repeticiones_internas = 0
    tiempo_total = 0.0

    if algoritmo == "recursivo" or len(X) > 200:

        inicio = time.thread_time()
        resultado = ejecutar(algoritmo, X, Y)
        tiempo_total = time.thread_time() - inicio

        repeticiones_internas = 1

    else:

        inicio = time.thread_time()

        while True:

            resultado = ejecutar(algoritmo, X, Y)
            repeticiones_internas += 1

            tiempo_total = time.thread_time() - inicio

            if tiempo_total >= 0.2:
                break

            if repeticiones_internas >= 100000:
                break

    tiempo_cpu = tiempo_total / repeticiones_internas


    # La medición con tracemalloc rastrea asignaciones de Python;
    # no representa necesariamente toda la memoria del proceso.
    # MEDICION DE MEMORIA POR SEPARADO
    tracemalloc.start()

    resultado = ejecutar(algoritmo, X, Y)

    actual, pico = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return {
        "algoritmo": algoritmo,
        "longitud": len(X),
        "tiempo_cpu": tiempo_cpu,
        "repeticiones_internas": repeticiones_internas,
        "memoria_pico_bytes": pico,
        "memoria_pico_kib": pico / 1024,
        "longitud_lcs": len(resultado),
        "resultado_lcs": resultado
    }


if __name__ == "__main__":

    algoritmo = sys.argv[1]
    X = sys.argv[2]
    Y = sys.argv[3]

    datos = medir(algoritmo, X, Y)

    print(json.dumps(datos))
