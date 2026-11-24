from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
ARCHIVO_ENTRADA = RAIZ_PROYECTO / "datos" / "crudo" / "datos.xlsx"
ARCHIVO_SALIDA = RAIZ_PROYECTO / "docs" / "graficos" / "cambio_tiempo.html"
COLUMNAS = ["Años__ESTANDAR", "value", "País__ESTANDAR"]


def main():
    if not ARCHIVO_ENTRADA.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {ARCHIVO_ENTRADA}")

    datos = pd.read_excel(ARCHIVO_ENTRADA)
    faltantes = [columna for columna in COLUMNAS if columna not in datos.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas necesarias: {faltantes}")
    if datos[COLUMNAS].isna().any().any():
        raise ValueError("Hay valores faltantes en año, value o región.")
    if datos.empty:
        raise ValueError("El archivo de entrada no contiene observaciones.")

    datos["Años__ESTANDAR"] = pd.to_numeric(datos["Años__ESTANDAR"], errors="raise")
    datos["value"] = pd.to_numeric(datos["value"], errors="raise")
    if datos.duplicated(["Años__ESTANDAR", "País__ESTANDAR"]).any():
        raise ValueError("Hay más de una observación por año y región.")

    regiones = datos["País__ESTANDAR"].drop_duplicates().tolist()
    tabla = (
        datos.pivot(
            index="Años__ESTANDAR",
            columns="País__ESTANDAR",
            values="value",
        )
        .reindex(columns=regiones)
        .reset_index()
        .rename_axis(columns=None)
        .sort_values("Años__ESTANDAR")
    )
    fuente = "FAOSTAT"
    grafico = (
        alt.Chart(datos)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "Años__ESTANDAR:Q",
                title="Año",
                axis=alt.Axis(format="d", tickMinStep=1),
            ),
            y=alt.Y("value:Q", title="Variación de temperatura media (°C)"),
            color=alt.Color("País__ESTANDAR:N", title="Región", sort=regiones),
            tooltip=[
                alt.Tooltip("País__ESTANDAR:N", title="Región"),
                alt.Tooltip("Años__ESTANDAR:Q", title="Año", format="d"),
                alt.Tooltip("value:Q", title="Variación (°C)", format=".3f"),
            ],
        )
        .properties(
            width=850,
            height=460,
            title=alt.TitleParams(
                text="Evolución de la variación de temperatura por región",
                subtitle=[f"n = {len(datos)} observaciones", f"Fuente: {fuente}"],
            ),
        )
    )
    tabla_html = tabla.to_html(
        index=False,
        border=0,
        classes="tabla-datos",
        table_id="datos-grafico",
        float_format=lambda valor: format(valor, ".15g"),
    )
    pagina = grafico.to_html()
    seccion = f"""
<section class="detalle">
  <h2>Por qué es adecuado</h2>
  <p>El gráfico de líneas respeta el orden temporal de los años y permite comparar la trayectoria observada en cada región. Las líneas conectan las observaciones anuales disponibles; no implican una relación causal.</p>
  <h2>Datos usados para el gráfico</h2>
  <p>Fuente: {fuente}. La tabla presenta los valores por año y región.</p>
  {tabla_html}
</section>
<style>
  body {{ font-family: sans-serif; margin: 2rem; }}
  .detalle {{ max-width: 1100px; margin: 2rem auto; line-height: 1.5; }}
  .tabla-datos {{ border-collapse: collapse; width: 100%; }}
  .tabla-datos th, .tabla-datos td {{ border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: right; }}
  .tabla-datos th {{ position: sticky; top: 0; background: #f2f2f2; }}
</style>
"""
    pagina = pagina.replace("</body>", f"{seccion}</body>")

    ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVO_SALIDA.write_text(pagina, encoding="utf-8")
    print(f"Observaciones: {len(datos)}; regiones: {len(regiones)}")
    print(f"Años: {int(datos['Años__ESTANDAR'].min())}–{int(datos['Años__ESTANDAR'].max())}")
    print(f"Gráfico guardado en: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    main()
