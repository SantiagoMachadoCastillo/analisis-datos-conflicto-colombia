from pathlib import Path

import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
ARCHIVO = RAIZ_PROYECTO / "datos" / "crudo" / "datos.xlsx"
REPORTE = RAIZ_PROYECTO / "docs" / "reporte_carga.md"
INDICADORES_TEXTO_DANADO = ("Ã", "Â", "�", "â€")


def celda_markdown(valor):
    if pd.isna(valor):
        return "NaN"
    return str(valor).replace("|", r"\|").replace("\r\n", "\n").replace("\n", "<br>")


def tabla_markdown(columnas, filas):
    encabezado = "| " + " | ".join(celda_markdown(columna) for columna in columnas) + " |"
    separador = "| " + " | ".join("---" for _ in columnas) + " |"
    cuerpo = [
        "| " + " | ".join(celda_markdown(valor) for valor in fila) + " |"
        for fila in filas
    ]
    return "\n".join([encabezado, separador, *cuerpo])


def main():
    if not ARCHIVO.is_file():
        raise FileNotFoundError(f"No se encontró el archivo solicitado: {ARCHIVO}")

    datos = pd.read_excel(ARCHIVO)
    primeras_filas = datos.head(5)
    filas_vacias = int(datos.isna().all(axis=1).sum())
    textos = [str(valor) for valor in datos.columns]
    textos.extend(datos.astype("string").fillna("").to_numpy().ravel().tolist())
    texto_danado = any(
        indicador in texto
        for texto in textos
        for indicador in INDICADORES_TEXTO_DANADO
    )

    problemas = [
        (
            "Posibles caracteres dañados (por ejemplo, tildes o eñes): "
            + ("sí; se encontraron indicadores sospechosos." if texto_danado else "no detectados.")
        ),
        "Separador: no aplica (archivo Excel).",
        f"Filas completamente vacías leídas: {filas_vacias}.",
    ]
    tipos = [
        f"| `{celda_markdown(columna)}` | `{tipo}` |"
        for columna, tipo in zip(datos.columns, datos.dtypes)
    ]
    reporte = "\n".join(
        [
            "# Reporte de carga",
            "",
            "Archivo leído con pandas: `datos/crudo/datos.xlsx`.",
            "",
            "## Dimensiones",
            "",
            f"- Filas: {len(datos)}",
            f"- Columnas: {len(datos.columns)}",
            "",
            "## Nombres exactos de las columnas",
            "",
            *[f"- `{celda_markdown(columna)}`" for columna in datos.columns],
            "",
            "## Tipos de datos",
            "",
            "| Columna | Tipo reportado por pandas |",
            "| --- | --- |",
            *tipos,
            "",
            "## Primeras 5 filas",
            "",
            tabla_markdown(datos.columns, primeras_filas.itertuples(index=False, name=None)),
            "",
            "## Posibles problemas de lectura",
            "",
            *[f"- {problema}" for problema in problemas],
            "",
        ]
    )
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text(reporte, encoding="utf-8")
    print(reporte, end="")
    print(f"\nReporte guardado en: {REPORTE}")


if __name__ == "__main__":
    main()
