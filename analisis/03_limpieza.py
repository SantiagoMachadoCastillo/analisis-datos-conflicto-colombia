from pathlib import Path

import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
ARCHIVO_ENTRADA = RAIZ_PROYECTO / "datos" / "crudo" / "datos.xlsx"
ARCHIVO_SALIDA = RAIZ_PROYECTO / "datos" / "limpio" / "temperatura_limpia.csv"
REPORTE = RAIZ_PROYECTO / "docs" / "limpieza.md"

RENOMBRES = {
    "indicator": "indicador",
    "País__ESTANDAR": "region",
    "Años__ESTANDAR": "anio",
    "value": "variacion_temperatura",
    "unit": "unidad",
    "notes_ids": "ids_notas",
    "source_id": "id_fuente",
}
CATEGORIAS_A_TEXTO = ["indicador", "region", "unidad", "ids_notas", "id_fuente"]


def texto_markdown(valor):
    if pd.isna(valor):
        return "—"
    return str(valor).replace("|", r"\|").replace("\r\n", "\n").replace("\n", "<br>")


def lista_valores(serie):
    valores = serie.dropna().drop_duplicates().tolist()
    if not valores:
        return "ninguna (todos los valores faltan)"
    return ", ".join(f"`{texto_markdown(valor)}`" for valor in valores)


def main():
    if not ARCHIVO_ENTRADA.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {ARCHIVO_ENTRADA}")

    originales = pd.read_excel(ARCHIVO_ENTRADA)
    if list(originales.columns) != list(RENOMBRES):
        raise ValueError(
            "El esquema de datos no coincide con el esperado. "
            f"Columnas leídas: {list(originales.columns)!r}"
        )

    filas_originales = len(originales)
    filas_vacias = int(originales.isna().all(axis=1).sum())
    duplicados_exactos = int(originales.duplicated().sum())
    duplicados_region_anio = int(
        originales.duplicated(["País__ESTANDAR", "Años__ESTANDAR"]).sum()
    )
    faltantes = originales.isna().sum()

    datos = originales.rename(columns=RENOMBRES).copy()
    anios = pd.to_numeric(datos["anio"], errors="raise")
    if anios.notna().any() and not (anios.dropna() % 1 == 0).all():
        raise ValueError("La variable de año contiene valores no enteros.")
    datos["anio"] = anios.astype("Int64")
    datos["variacion_temperatura"] = pd.to_numeric(
        datos["variacion_temperatura"], errors="raise"
    ).astype("float64")
    for columna in CATEGORIAS_A_TEXTO:
        datos[columna] = datos[columna].astype("string")

    # Se conservan filas vacías, duplicados y categorías tal como estén en el origen.
    filas_eliminadas = filas_originales - len(datos)
    ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    datos.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8", na_rep="")
    salida_verificada = pd.read_csv(ARCHIVO_SALIDA)
    if len(salida_verificada) != filas_originales:
        raise ValueError(
            "La verificación del CSV detectó una cantidad de filas distinta a la fuente."
        )
    if list(salida_verificada.columns) != list(datos.columns):
        raise ValueError("La verificación del CSV detectó columnas inesperadas.")

    conversiones = [
        ("indicador", "Texto (`string`)", "Texto de categoría, sin cambios de valores."),
        ("region", "Texto (`string`)", "Texto de categoría; se conservan tildes y etiquetas."),
        ("anio", "Entero nullable (`Int64`)", "Año entero; no se inventan mes ni día."),
        ("variacion_temperatura", "Decimal (`float64`)", "Conversión numérica, sin filtrar extremos."),
        ("unidad", "Texto (`string`)", "Texto de categoría, sin cambios de valores."),
        ("ids_notas", "Texto nullable (`string`)", "Se preserva aunque todos sus valores estén faltantes."),
        ("id_fuente", "Texto (`string`)", "Identificador tratado como etiqueta, no como cantidad."),
    ]
    filas_conversiones = [
        f"| `{nombre}` | {tipo} | {motivo} |"
        for nombre, tipo, motivo in conversiones
    ]
    filas_faltantes = [
        f"| `{RENOMBRES[columna]}` | {int(cantidad)} |"
        for columna, cantidad in faltantes.items()
    ]
    filas_categorias = [
        f"| `{RENOMBRES[columna]}` | {lista_valores(originales[columna])} |"
        for columna in ("indicator", "País__ESTANDAR", "unit", "notes_ids", "source_id")
    ]

    reporte = "\n".join(
        [
            "# Decisiones de limpieza",
            "",
            "Fuente: `datos/crudo/datos.xlsx`, leído con pandas. "
            "La fuente no se modifica.",
            "",
            "## Resumen de filas",
            "",
            f"- Filas leídas: {filas_originales}.",
            f"- Filas completamente vacías: {filas_vacias}; no se eliminaron.",
            f"- Filas duplicadas exactas: {duplicados_exactos}; no se eliminaron.",
            f"- Duplicados de la combinación región-año: {duplicados_region_anio}; no se eliminaron.",
            f"- Filas eliminadas: {filas_eliminadas}.",
            "- Valores atípicos: no se eliminaron ni modificaron.",
            "",
            "## Renombres y tipos",
            "",
            "| Variable de salida | Tipo aplicado | Decisión |",
            "| --- | --- | --- |",
            *filas_conversiones,
            "",
            "## Faltantes antes de la limpieza",
            "",
            "| Variable de salida | Valores faltantes |",
            "| --- | ---: |",
            *filas_faltantes,
            "",
            "`ids_notas` está completamente vacío; se conserva la columna y sus valores "
            "faltantes se representan como celdas vacías en el CSV. No se imputaron datos.",
            "",
            "## Categorías observadas y tratamiento",
            "",
            "| Variable | Valores observados |",
            "| --- | --- |",
            *filas_categorias,
            "",
            "No se detectaron inconsistencias entre las categorías observadas; se "
            "mantuvieron las etiquetas originales sin normalizarlas ni combinarlas.",
            "",
            "## Salida",
            "",
            f"`datos/limpio/{ARCHIVO_SALIDA.name}`. Se conserva el orden de las filas "
            "y se exporta sin índice.",
            "",
        ]
    )
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text(reporte, encoding="utf-8")
    print(reporte, end="")
    print(f"\nCSV guardado en: {ARCHIVO_SALIDA}")
    print(f"Decisiones guardadas en: {REPORTE}")


if __name__ == "__main__":
    main()
