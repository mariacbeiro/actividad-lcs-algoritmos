"""Pruebas que comparan la validez y la longitud de las tres soluciones."""


from recursivo import lcs_recursivo
from hirschberg import hirschberg
from dinamico import lcs_dinamico
from test_recursivo import es_subsecuencia


def ejecutar_pruebas():

    """Verifica que las tres implementaciones dan LCS válidas y óptimas."""

    casos = [
        ("ABC", "AC", 2),
        ("ABC", "ABC", 3),
        ("ABC", "XYZ", 0),
        ("ABC", "", 0),
        ("", "", 0),
        ("AAB", "AB", 2),
        ("ABC", "BAC", 2),
        ("ABCD", "ACBD", 3),
        ("AAAA", "AA", 2),
        ("AGGTAB", "GXTXAYB", 4),
        ("XMJYAUZ", "MZJAWXU", 4),
    ]

    for numero, (X, Y, esperado) in enumerate(casos, 1):

        resultado_a = lcs_recursivo(
            X, Y, len(X), len(Y)
        )

        resultado_b = hirschberg(X, Y)
        resultado_c = lcs_dinamico(X, Y)

        resultados = {
            "Recursivo": resultado_a,
            "Hirschberg": resultado_b,
            "Dinamico": resultado_c
        }

        for nombre, resultado in resultados.items():

            assert es_subsecuencia(resultado, X), (
                f"{nombre}: resultado no valido para X"
            )

            assert es_subsecuencia(resultado, Y), (
                f"{nombre}: resultado no valido para Y"
            )

            assert len(resultado) == esperado, (
                f"{nombre}: longitud incorrecta"
            )

        assert (
            len(resultado_a)
            == len(resultado_b)
            == len(resultado_c)
        )

        print(f"Prueba {numero}: CORRECTA")
        print(f"  X: {X}")
        print(f"  Y: {Y}")
        print(f"  Recursivo: {resultado_a}")
        print(f"  Hirschberg: {resultado_b}")
        print(f"  Dinamico: {resultado_c}")
        print()

    print("TODAS LAS PRUEBAS SUPERADAS")


if __name__ == "__main__":
    ejecutar_pruebas()
