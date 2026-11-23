"""Cálculo de LCS mediante una tabla completa de programación dinámica.

Primero obtiene las longitudes óptimas y después reconstruye la subsecuencia."""


def lcs_dinamico(X, Y):
    """Devuelve una LCS de X e Y mediante una tabla de longitudes.

La tabla tiene (m + 1) x (n + 1) posiciones. Después se recorre
hacia atrás para recuperar una subsecuencia óptima."""

    m = len(X)
    n = len(Y)

    # Crear tabla de (m+1) filas y (n+1) columnas
    tabla = [
        [0] * (n + 1)
        for _ in range(m + 1)
    ]

    # Rellenar la tabla
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if X[i - 1] == Y[j - 1]:
                tabla[i][j] = tabla[i - 1][j - 1] + 1

            else:
                tabla[i][j] = max(
                    tabla[i - 1][j],
                    tabla[i][j - 1]
                )

    # Reconstruir la subsecuencia
    i = m
    j = n
    resultado = []

    while i > 0 and j > 0:

        if X[i - 1] == Y[j - 1]:
            resultado.append(X[i - 1])
            i -= 1
            j -= 1

        elif tabla[i - 1][j] >= tabla[i][j - 1]:
            i -= 1

        else:
            j -= 1

    # Invertir los caracteres encontrados
    resultado.reverse()

    return "".join(resultado)


if __name__ == "__main__":
    X = "ABC"
    Y = "AC"

    resultado = lcs_dinamico(X, Y)

    print("Cadena X:", X)
    print("Cadena Y:", Y)
    print("LCS:", resultado)
    print("Longitud:", len(resultado))
