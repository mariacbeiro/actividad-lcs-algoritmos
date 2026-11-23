"""Algoritmo de Hirschberg para obtener una subsecuencia común más larga.

Combina divide y vencerás con filas de programación dinámica para reducir memoria."""


def lcs_longitudes(X, inicio_x, fin_x,
                   Y, inicio_y, fin_y, inverso=False):
    """Calcula la última fila de longitudes LCS para dos fragmentos.

Usa únicamente la fila anterior y la actual. Si inverso es True,
recorre ambos fragmentos desde el final sin crear copias."""

    n = fin_y - inicio_y
    anterior = [0] * (n + 1)

    for i in range(fin_x - inicio_x):
        actual = [0] * (n + 1)

        if inverso:
            caracter_x = X[fin_x - 1 - i]
        else:
            caracter_x = X[inicio_x + i]

        for j in range(1, n + 1):
            if inverso:
                caracter_y = Y[fin_y - j]
            else:
                caracter_y = Y[inicio_y + j - 1]

            if caracter_x == caracter_y:
                actual[j] = anterior[j - 1] + 1
            else:
                actual[j] = max(
                    anterior[j],
                    actual[j - 1]
                )

        anterior = actual

    return anterior


def _hirschberg(X, inicio_x, fin_x,
                Y, inicio_y, fin_y):
    """Resuelve LCS recursivamente sobre rangos de índices.

Divide X en dos mitades y elige el corte de Y que maximiza la
suma de las longitudes LCS calculadas en ambos sentidos."""

    m = fin_x - inicio_x
    n = fin_y - inicio_y

    # Caso base: cadena vacía
    if m == 0 or n == 0:
        return ""

    # Caso base: X tiene un carácter
    if m == 1:
        caracter = X[inicio_x]

        for j in range(inicio_y, fin_y):
            if Y[j] == caracter:
                return caracter

        return ""

    # Caso base: Y tiene un carácter
    if n == 1:
        caracter = Y[inicio_y]

        for i in range(inicio_x, fin_x):
            if X[i] == caracter:
                return caracter

        return ""

    # Dividir X por la mitad
    mitad = inicio_x + m // 2

    # Longitudes hacia delante
    L1 = lcs_longitudes(
        X, inicio_x, mitad,
        Y, inicio_y, fin_y
    )

    # Longitudes hacia atrás
    L2 = lcs_longitudes(
        X, mitad, fin_x,
        Y, inicio_y, fin_y,
        inverso=True
    )

    # Encontrar el mejor corte de Y
    mejor_corte = 0
    mejor_valor = -1

    for j in range(n + 1):
        valor = L1[j] + L2[n - j]

        if valor > mejor_valor:
            mejor_valor = valor
            mejor_corte = j

    # Evitar que ambas filas permanezcan en memoria mientras se
    # resuelven los subproblemas recursivos.
    # Liberar las filas antes de la recursión
    del L1
    del L2

    corte_y = inicio_y + mejor_corte

    # Resolver los dos subproblemas
    resultado_izquierdo = _hirschberg(
        X, inicio_x, mitad,
        Y, inicio_y, corte_y
    )

    resultado_derecho = _hirschberg(
        X, mitad, fin_x,
        Y, corte_y, fin_y
    )

    return resultado_izquierdo + resultado_derecho


def hirschberg(X, Y):
    """Devuelve una LCS completa, situando la cadena menor como Y.

Así se minimiza el ancho de las filas auxiliares."""

    if len(Y) > len(X):
        X, Y = Y, X

    return _hirschberg(
        X, 0, len(X),
        Y, 0, len(Y)
    )


if __name__ == "__main__":
    X = "ABCD"
    Y = "ACBD"

    resultado = hirschberg(X, Y)

    print("Cadena X:", X)
    print("Cadena Y:", Y)
    print("LCS:", resultado)
    print("Longitud:", len(resultado))
