# Reporte de carga

Archivo leído con pandas: `datos/crudo/datos.xlsx`.

## Dimensiones

- Filas: 195
- Columnas: 7

## Nombres exactos de las columnas

- `indicator`
- `País__ESTANDAR`
- `Años__ESTANDAR`
- `value`
- `unit`
- `notes_ids`
- `source_id`

## Tipos de datos

| Columna | Tipo reportado por pandas |
| --- | --- |
| `indicator` | `str` |
| `País__ESTANDAR` | `str` |
| `Años__ESTANDAR` | `int64` |
| `value` | `float64` |
| `unit` | `str` |
| `notes_ids` | `float64` |
| `source_id` | `int64` |

## Primeras 5 filas

| indicator | País__ESTANDAR | Años__ESTANDAR | value | unit | notes_ids | source_id |
| --- | --- | --- | --- | --- | --- | --- |
| Variación de la temperatura media | El Caribe | 1961 | -0.039 | Grados celsius | NaN | 651 |
| Variación de la temperatura media | El Caribe | 1962 | -0.059 | Grados celsius | NaN | 651 |
| Variación de la temperatura media | El Caribe | 1963 | -0.079 | Grados celsius | NaN | 651 |
| Variación de la temperatura media | El Caribe | 1964 | 0.132 | Grados celsius | NaN | 651 |
| Variación de la temperatura media | El Caribe | 1965 | -0.096 | Grados celsius | NaN | 651 |

## Posibles problemas de lectura

- Posibles caracteres dañados (por ejemplo, tildes o eñes): no detectados.
- Separador: no aplica (archivo Excel).
- Filas completamente vacías leídas: 0.
