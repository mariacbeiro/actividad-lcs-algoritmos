"""Punto de entrada del proyecto: pruebas y experimentos opcionales."""


import sys

from test_recursivo import ejecutar_pruebas as test_recursivo
from test_hirschberg import ejecutar_pruebas as test_hirschberg
from test_comparacion import ejecutar_pruebas as test_comparacion
from experimentos import ejecutar_experimentos


def main():
    """Ejecuta los tests y, si se solicita, también los experimentos."""

    print("PROYECTO LCS - DISEÑO AVANZADO DE ALGORITMOS")

    print("\n1. Pruebas del algoritmo recursivo")
    test_recursivo()

    print("\n2. Pruebas de Hirschberg")
    test_hirschberg()

    print("\n3. Pruebas comparativas")
    test_comparacion()

    # Por defecto solo se ejecutan las pruebas rápidas.
    # La campaña completa se activa expresamente con --experimentos.
    if "--experimentos" in sys.argv:
        print("\n4. Ejecutando experimentos")
        ejecutar_experimentos()

    print("\nPROCESO FINALIZADO CORRECTAMENTE")


if __name__ == "__main__":
    main()
