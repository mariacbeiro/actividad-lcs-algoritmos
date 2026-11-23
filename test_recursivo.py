"""Pruebas funcionales de la implementación recursiva directa de LCS."""


from recursivo import lcs_recursivo

# Creamos función para comprobar resultado
def es_subsecuencia(subsecuencia, cadena):
    """Verifica que la subsecuencia mantiene el orden de la cadena."""

    posicion = 0

    for caracter in cadena:
        if posicion < len(subsecuencia):
            if caracter == subsecuencia[posicion]:
                posicion += 1

    return posicion == len(subsecuencia)


def ejecutar_pruebas():
    """Ejecuta casos conocidos y comprueba longitud y validez."""

    casos = [
        ("ABC", "AC", 2),
        ("ABC", "ABC", 3),
        ("ABC", "XYZ", 0),
        ("ABC", "", 0),
        ("AAB", "AB", 2),
        ("ABC", "BAC", 2),
    ]

    for numero, (X, Y, longitud_esperada) in enumerate(casos, 1):
        resultado = lcs_recursivo(X, Y, len(X), len(Y))

        assert len(resultado) == longitud_esperada
        assert es_subsecuencia(resultado, X)
        assert es_subsecuencia(resultado, Y)

        print(f"Prueba {numero}: CORRECTA")
        print(f"  X = {X}")
        print(f"  Y = {Y}")
        print(f"  LCS = {resultado}")
        print()


if __name__ == "__main__":
    ejecutar_pruebas()
