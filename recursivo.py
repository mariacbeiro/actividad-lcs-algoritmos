"""Implementación recursiva directa de LCS, sin memorización.

Explora subproblemas repetidos; se utiliza como referencia de coste exponencial."""


def lcs_recursivo(X, Y, i, j):
    # Caso base: alguna cadena está vacía
    """Devuelve una LCS de X[:i] e Y[:j] mediante recursión directa.

Cuando los caracteres finales no coinciden, explora ambas alternativas
sin guardar resultados intermedios."""

    if i == 0 or j == 0:
        return ""

    # Si los últimos caracteres coinciden
    if X[i - 1] == Y[j - 1]:
        return lcs_recursivo(X, Y, i - 1, j - 1) + X[i - 1]

    # Si no coinciden, exploramos ambas opciones
    opcion1 = lcs_recursivo(X, Y, i - 1, j)
    opcion2 = lcs_recursivo(X, Y, i, j - 1)

    # Devolvemos la subsecuencia más larga
    if len(opcion1) >= len(opcion2):
        return opcion1
    else:
        return opcion2


# Prueba inicial
if __name__ == "__main__":
    X = "ABC"
    Y = "BAC"

    resultado = lcs_recursivo(X, Y, len(X), len(Y))

    print("Cadena X:", X)
    print("Cadena Y:", Y)
    print("LCS:", resultado)
    print("Longitud:", len(resultado))
