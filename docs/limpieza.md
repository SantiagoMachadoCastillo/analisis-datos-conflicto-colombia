# Decisiones de limpieza

Fuente: `datos/crudo/datos.xlsx`, leído con pandas. La fuente no se modifica.

## Resumen de filas

- Filas leídas: 195.
- Filas completamente vacías: 0; no se eliminaron.
- Filas duplicadas exactas: 0; no se eliminaron.
- Duplicados de la combinación región-año: 0; no se eliminaron.
- Filas eliminadas: 0.
- Valores atípicos: no se eliminaron ni modificaron.

## Renombres y tipos

| Variable de salida | Tipo aplicado | Decisión |
| --- | --- | --- |
| `indicador` | Texto (`string`) | Texto de categoría, sin cambios de valores. |
| `region` | Texto (`string`) | Texto de categoría; se conservan tildes y etiquetas. |
| `anio` | Entero nullable (`Int64`) | Año entero; no se inventan mes ni día. |
| `variacion_temperatura` | Decimal (`float64`) | Conversión numérica, sin filtrar extremos. |
| `unidad` | Texto (`string`) | Texto de categoría, sin cambios de valores. |
| `ids_notas` | Texto nullable (`string`) | Se preserva aunque todos sus valores estén faltantes. |
| `id_fuente` | Texto (`string`) | Identificador tratado como etiqueta, no como cantidad. |

## Faltantes antes de la limpieza

| Variable de salida | Valores faltantes |
| --- | ---: |
| `indicador` | 0 |
| `region` | 0 |
| `anio` | 0 |
| `variacion_temperatura` | 0 |
| `unidad` | 0 |
| `ids_notas` | 195 |
| `id_fuente` | 0 |

`ids_notas` está completamente vacío; se conserva la columna y sus valores faltantes se representan como celdas vacías en el CSV. No se imputaron datos.

## Categorías observadas y tratamiento

| Variable | Valores observados |
| --- | --- |
| `indicador` | `Variación de la temperatura media` |
| `region` | `El Caribe`, `América Central`, `América del Sur` |
| `unidad` | `Grados celsius` |
| `ids_notas` | ninguna (todos los valores faltan) |
| `id_fuente` | `651` |

No se detectaron inconsistencias entre las categorías observadas; se mantuvieron las etiquetas originales sin normalizarlas ni combinarlas.

## Salida

`datos/limpio/temperatura_limpia.csv`. Se conserva el orden de las filas y se exporta sin índice.
