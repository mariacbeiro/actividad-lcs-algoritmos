"""Generación reproducible de las cadenas usadas en los experimentos.

Las semillas fijas permiten repetir exactamente las mismas entradas."""


import random


def generar_casos():
    """Genera diez parejas de cadenas de igual longitud y reproducibles.

Cada longitud tiene una semilla fija propia; se utiliza el alfabeto ABCD."""

    longitudes = [10, 12, 15, 16, 18, 20, 50, 200, 500, 1000]
    alfabeto = "ABCD"

    casos = []

    for longitud in longitudes:

        # Semilla fija para reproducir los datos
        generador = random.Random(2026 + longitud)

        X = "".join(
            generador.choice(alfabeto)
            for _ in range(longitud)
        )

        Y = "".join(
            generador.choice(alfabeto)
            for _ in range(longitud)
        )

        casos.append((longitud, X, Y))

    return casos


if __name__ == "__main__":

    casos = generar_casos()

    for longitud, X, Y in casos:
        print(f"Longitud: {longitud}")
        print(f"  X: {X[:30]}...")
        print(f"  Y: {Y[:30]}...")
        print()
