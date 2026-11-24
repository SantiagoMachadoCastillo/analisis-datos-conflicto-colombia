from pathlib import Path

import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
ARCHIVO = RAIZ_PROYECTO / "datos" / "crudo" / "datos.xlsx"
REPORTE = RAIZ_PROYECTO / "docs" / "inventario.md"
TIPOS_PROPUESTOS = {
    "indicator": "Nominal",
    "País__ESTANDAR": "Nominal",
    "Años__ESTANDAR": "Fecha",
    "value": "Numérica",
    "unit": "Nominal",
    "notes_ids": "Nominal",
    "source_id": "Nominal",
}
CANTIDAD_EJEMPLOS = 5


def formato_markdown(valor):
    if pd.isna(valor):
        return "—"
    return str(valor).replace("|", r"\|").replace("\r\n", "\n").replace("\n", "<br>")


def tabla_markdown(filas):
    encabezado = (
        "| Nombre de variable | Tipo de dato propuesto | Valores válidos (n) "
        "| Valores faltantes (n) | Categorías distintas (n) | Ejemplos |"
    )
    separador = "| --- | --- | ---: | ---: | ---: | --- |"
    cuerpo = [
        "| " + " | ".join(formato_markdown(valor) for valor in fila) + " |"
        for fila in filas
    ]
    return "\n".join([encabezado, separador, *cuerpo])


def main():
    if not ARCHIVO.is_file():
        raise FileNotFoundError(f"No se encontró el archivo solicitado: {ARCHIVO}")

    datos = pd.read_excel(ARCHIVO)
    variables_sin_clasificar = [
        columna for columna in datos.columns if columna not in TIPOS_PROPUESTOS
    ]
    if variables_sin_clasificar:
        raise ValueError(
            "Falta proponer un tipo para estas variables: "
            + ", ".join(str(columna) for columna in variables_sin_clasificar)
        )

    filas = []
    for variable in datos.columns:
        valores = datos[variable]
        validos = valores.dropna()
        ejemplos = list(pd.unique(validos)[:CANTIDAD_EJEMPLOS])
        filas.append(
            [
                variable,
                TIPOS_PROPUESTOS[variable],
                len(validos),
                int(valores.isna().sum()),
                int(valores.nunique(dropna=True)),
                ", ".join(formato_markdown(valor) for valor in ejemplos) or "—",
            ]
        )

    reporte = "\n".join(
        [
            "# Inventario de variables",
            "",
            "Fuente: `datos/crudo/datos.xlsx`, leído con pandas.",
            "",
            "La clasificación es una propuesta semántica. "
            "Los valores válidos son los registros no faltantes; "
            "no se realizó una validación de contenido ni se limpiaron datos. "
            "Los ejemplos son hasta cinco valores distintos, en orden de aparición.",
            "",
            "La variable `Años__ESTANDAR` se clasifica como `Fecha` por representar "
            "años, aunque el archivo la almacena como número entero.",
            "",
            tabla_markdown(filas),
            "",
        ]
    )
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text(reporte, encoding="utf-8")
    print(reporte, end="")
    print(f"\nInventario guardado en: {REPORTE}")


if __name__ == "__main__":
    main()
