# Inventario de variables

Fuente: `datos/crudo/datos.xlsx`, leído con pandas.

La clasificación es una propuesta semántica. Los valores válidos son los registros no faltantes; no se realizó una validación de contenido ni se limpiaron datos. Los ejemplos son hasta cinco valores distintos, en orden de aparición.

La variable `Años__ESTANDAR` se clasifica como `Fecha` por representar años, aunque el archivo la almacena como número entero.

| Nombre de variable | Tipo de dato propuesto | Valores válidos (n) | Valores faltantes (n) | Categorías distintas (n) | Ejemplos |
| --- | --- | ---: | ---: | ---: | --- |
| indicator | Nominal | 195 | 0 | 1 | Variación de la temperatura media |
| País__ESTANDAR | Nominal | 195 | 0 | 3 | El Caribe, América Central, América del Sur |
| Años__ESTANDAR | Fecha | 195 | 0 | 65 | 1961, 1962, 1963, 1964, 1965 |
| value | Numérica | 195 | 0 | 180 | -0.039, -0.059, -0.079, 0.132, -0.096 |
| unit | Nominal | 195 | 0 | 1 | Grados celsius |
| notes_ids | Nominal | 0 | 195 | 0 | — |
| source_id | Nominal | 195 | 0 | 1 | 651 |
