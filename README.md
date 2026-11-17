# analisis-datos-conflicto-colombia
Este codespace trata sobre un dataset que muestra la temperatura promedio de varias regiones de América (América Central, Del Sur y El Caribe) y su evolución a lo largo de los años.

# Análisis de la variación de la temperatura media en América Latina (1961-2025)

## 1. ¿Cuál es el análisis de datos?

Este proyecto busca analizar la evolución de la variación de la temperatura media en tres regiones de América Latina: El Caribe, América Central y América del Sur, durante el periodo comprendido entre 1961 y 2025.

A partir de los datos recopilados, se pretende identificar los cambios que ha presentado la variación de temperatura a lo largo del tiempo, comparar el comportamiento de las tres regiones y reconocer los años en los que se registraron los valores más altos y más bajos.

El propósito es comprender las diferencias regionales y las tendencias observables en el comportamiento de la temperatura, utilizando herramientas de análisis estadístico y visualización de datos.

### Pregunta principal

¿Cómo ha evolucionado la variación de la temperatura media en El Caribe, América Central y América del Sur entre 1961 y 2025, y qué diferencias se pueden identificar entre estas regiones?

### Preguntas orientadoras

- ¿Cómo ha cambiado la variación de la temperatura media en las tres regiones a lo largo de los años?
- ¿Qué región presenta los valores más altos de variación de temperatura?
- ¿En qué años se registraron los valores máximos y mínimos de cada región?
- ¿Qué diferencias existen entre el comportamiento de la temperatura de las tres regiones?
- ¿Se observa una tendencia general de aumento en la variación de temperatura durante el periodo estudiado?

## 2. Descripción de los datos

El dataset contiene 195 registros correspondientes a la variación anual de la temperatura media en tres regiones de América Latina: El Caribe, América Central y América del Sur.

La información comprende 65 años, desde 1961 hasta 2025, con una observación por cada región en cada año.

Los datos están expresados en grados Celsius (°C) y corresponden a variaciones de temperatura respecto al periodo de referencia 1951-1980. Por lo tanto, no representan temperaturas absolutas.

### Variables del dataset

| Variable | Descripción | Tipo |
|---|---|---|
| indicator | Nombre del indicador estudiado. | Categórica nominal |
| País__ESTANDAR | Región geográfica del registro. | Categórica nominal |
| Años__ESTANDAR | Año al que corresponde el registro. | Fecha/temporal |
| value | Valor de la variación de temperatura. | Numérica |
| unit | Unidad de medida. | Categórica nominal |
| notes_ids | Identificador de notas adicionales. | Categórica nominal |
| source_id | Identificador de la fuente de información. | Categórica nominal |

### Cobertura geográfica

- El Caribe.
- América Central.
- América del Sur.

### Periodo de estudio

1961-2025.

### Fuente de información

CEPALSTAT (Comisión Económica para América Latina y el Caribe), con referencia a FAOSTAT y al conjunto de datos GISTEMP de NASA-GISS.

### Unidad de medida

Grados Celsius (°C).

### Periodicidad

Anual.

# Variación de la temperatura media en América Latina y el Caribe (1961\-2025)

## ¿Cuál es el análisis de datos?

Este proyecto analiza la evolución de la variación de la temperatura media en tres regiones de América Latina y el Caribe: El Caribe, América Central y América del Sur. La pregunta principal es:

**¿Cómo ha cambiado la variación de la temperatura media entre 1961 y 2025 y qué diferencias existen entre las regiones?**

El proyecto explora tendencias temporales, diferencias entre regiones y la relación entre los cambios observados en distintas zonas geográficas utilizando datos históricos publicados por CEPALSTAT y FAOSTAT.

## Descripción de los datos

Cada fila representa una observación anual para una región.

- Número de observaciones: 195
- Cobertura temporal: 1961\-2025
- Regiones analizadas: 
    - El Caribe
    - América Central
    - América del Sur
- Unidad de medida: Grados Celsius
- Fuente: CEPALSTAT con datos de FAOSTAT (FAO)

### Variables

| Variable | Descripción |
| --- | --- |
| indicator | Nombre del indicador analizado |
| País\_\_ESTANDAR | Región geográfica |
| Años\_\_ESTANDAR | Año de observación |
| value | Variación de la temperatura media |
| unit | Unidad de medida |
| notes\_ids | Identificador de notas asociadas |
| source\_id | Identificador de la fuente |

## Pregunta de investigación

¿Cómo ha evolucionado la variación de la temperatura media en América Latina y el Caribe durante los últimos 65 años y cuáles son las diferencias entre regiones?

## Fuente de datos

Comisión Económica para América Latina y el Caribe (CEPALSTAT) y Organización de las Naciones Unidas para la Alimentación y la Agricultura (FAO \- FAOSTAT).

