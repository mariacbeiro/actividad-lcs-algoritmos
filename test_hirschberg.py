"""Pruebas funcionales de Hirschberg con casos conocidos."""


from hirschberg import hirschberg
from test_recursivo import es_subsecuencia


def ejecutar_pruebas():
    """Comprueba Hirschberg con casos límite y longitudes conocidas."""

    casos = [
        ("ABC", "AC", 2),
        ("ABC", "ABC", 3),
        ("ABC", "XYZ", 0),
        ("ABC", "", 0),
        ("AAB", "AB", 2),
        ("ABC", "BAC", 2),
        ("ABCD", "ACBD", 3),
        ("AAAA", "AA", 2),
        ("", "", 0),
    ]

    for numero, (X, Y, longitud_esperada) in enumerate(casos, 1):
        resultado = hirschberg(X, Y)

        assert len(resultado) == longitud_esperada, (
            f"Longitud incorrecta en la prueba {numero}"
        )

        assert es_subsecuencia(resultado, X), (
            f"El resultado no es subsecuencia de X"
        )

        assert es_subsecuencia(resultado, Y), (
            f"El resultado no es subsecuencia de Y"
        )

        print(f"Prueba {numero}: CORRECTA")
        print(f"  X = {X}")
        print(f"  Y = {Y}")
        print(f"  LCS = {resultado}")
        print()


if __name__ == "__main__":
    ejecutar_pruebas()
