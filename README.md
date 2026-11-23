# Comparación de algoritmos para la subsecuencia común más larga (LCS)

Proyecto desarrollado para la Actividad 1 de la asignatura **Diseño Avanzado de Algoritmos**.

## Descripción

El proyecto implementa y compara tres algoritmos para calcular la subsecuencia común más larga (*Longest Common Subsequence*, LCS) de dos cadenas de caracteres.

Se han desarrollado tres soluciones:

- **Recursiva directa:** resuelve el problema mediante llamadas recursivas, sin memorización de resultados.
- **Hirschberg:** utiliza la estrategia de divide y vencerás para reducir la memoria auxiliar necesaria.
- **Programación dinámica tabular:** construye una tabla para almacenar las soluciones de los subproblemas y reconstruir la subsecuencia.

El objetivo es analizar las diferencias entre estos métodos en términos de tiempo de CPU y consumo máximo de memoria.

## Requisitos

- Python 3.12.
- No se necesitan librerías externas. Se utilizan únicamente módulos de la biblioteca estándar de Python.

## Ejecución

Para ejecutar las pruebas de funcionamiento, abrir una terminal en la carpeta del proyecto y escribir:

```bash
python main.py
```

Para ejecutar las pruebas y reproducir los experimentos:

```bash
python main.py --experimentos
```

La campaña experimental puede tardar varios minutos debido al elevado coste del algoritmo recursivo.

## Metodología experimental

Se generan diez parejas de cadenas de igual longitud, con tamaños de 10, 12, 15, 16, 18, 20, 50, 200, 500 y 1000 caracteres.

Las cadenas se construyen a partir del alfabeto `ABCD`, utilizando semillas fijas para que los datos puedan reproducirse.

Para cada algoritmo y longitud se realizan tres repeticiones. Se mide el tiempo de CPU y el pico de memoria rastreada mediante `tracemalloc`, calculando posteriormente la mediana de las ejecuciones completadas.

Cada ejecución tiene un límite de 120 segundos. Cuando la versión recursiva supera ese límite, se interrumpe y se omiten las pruebas recursivas de mayor longitud.

Los resultados se validan comprobando que la subsecuencia obtenida pertenece a ambas cadenas y que su longitud coincide con la solución óptima calculada mediante programación dinámica.

## Resultados

La carpeta `resultados/` contiene:

- `resultados_repeticiones_filtrados.csv`: mediciones individuales y estado de cada ejecución.
- `resultados_resumen_filtrados.csv`: medianas de tiempo de CPU y memoria para las ejecuciones completadas.

Los archivos CSV incluidos corresponden a la campaña utilizada para elaborar el informe.

Al volver a ejecutar los experimentos, el programa genera `resultados_repeticiones.csv` y `resultados_resumen.csv` en la carpeta principal. Estos archivos permiten comparar las nuevas mediciones con los resultados originales.

Los tiempos y consumos de memoria pueden variar según el equipo y el entorno de ejecución.

## Organización del código

| Archivo | Función |
|---|---|
| `main.py` | Ejecuta las pruebas y, opcionalmente, los experimentos. |
| `recursivo.py` | Implementación recursiva directa de LCS. |
| `hirschberg.py` | Implementación del algoritmo de Hirschberg. |
| `dinamico.py` | Implementación mediante programación dinámica tabular. |
| `generar_datos.py` | Generación reproducible de las cadenas. |
| `medir_algoritmo.py` | Medición del tiempo de CPU y la memoria. |
| `experimentos.py` | Ejecución de los experimentos y generación de los CSV. |
| `test_recursivo.py` | Pruebas de la versión recursiva. |
| `test_hirschberg.py` | Pruebas del algoritmo de Hirschberg. |
| `test_comparacion.py` | Comprobación y comparación de las tres implementaciones. |

## Observaciones

La versión recursiva presenta un crecimiento elevado del tiempo de ejecución, por lo que no resulta adecuada para cadenas grandes.

Hirschberg y la programación dinámica tabular ofrecen un comportamiento temporal mucho más favorable. La principal ventaja de Hirschberg es que necesita menos memoria auxiliar, mientras que la implementación tabular permite reconstruir la solución a partir de una tabla completa.

Las conclusiones se basan en las implementaciones y mediciones realizadas para esta actividad.