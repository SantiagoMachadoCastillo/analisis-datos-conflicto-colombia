from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
ARCHIVO_ENTRADA = RAIZ_PROYECTO / "datos" / "crudo" / "datos.xlsx"
ARCHIVO_SALIDA = RAIZ_PROYECTO / "docs" / "graficos" / "ranking.html"
COLUMNAS = ["País__ESTANDAR", "value"]


def main():
    if not ARCHIVO_ENTRADA.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {ARCHIVO_ENTRADA}")

    datos = pd.read_excel(ARCHIVO_ENTRADA)
    faltantes = [columna for columna in COLUMNAS if columna not in datos.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas necesarias: {faltantes}")
    if datos[COLUMNAS].isna().any().any():
        raise ValueError("Hay valores faltantes en región o value.")
    if datos.empty:
        raise ValueError("El archivo de entrada no contiene observaciones.")

    datos["value"] = pd.to_numeric(datos["value"], errors="raise")
    resumen = (
        datos.groupby("País__ESTANDAR", as_index=False, sort=False)
        .agg(promedio=("value", "mean"), n=("value", "count"))
        .sort_values("promedio", ascending=False, kind="stable")
    )
    if resumen.empty:
        raise ValueError("No hay regiones para comparar.")

    fuente = "FAOSTAT"
    barras = (
        alt.Chart(resumen)
        .mark_bar(color="#4C78A8")
        .encode(
            x=alt.X(
                "promedio:Q",
                title="Variación promedio de temperatura (°C)",
                scale=alt.Scale(zero=True),
            ),
            y=alt.Y(
                "País__ESTANDAR:N",
                title="Región",
                sort=alt.SortField(field="promedio", order="descending"),
            ),
            tooltip=[
                alt.Tooltip("País__ESTANDAR:N", title="Región"),
                alt.Tooltip("promedio:Q", title="Promedio (°C)", format=".6f"),
                alt.Tooltip("n:Q", title="Observaciones"),
            ],
        )
    )
    etiquetas = (
        alt.Chart(resumen)
        .mark_text(align="left", baseline="middle", dx=5, color="#222")
        .encode(
            x="promedio:Q",
            y=alt.Y(
                "País__ESTANDAR:N",
                sort=alt.SortField(field="promedio", order="descending"),
            ),
            text=alt.Text("promedio:Q", format=".4f"),
        )
    )
    grafico = alt.layer(barras, etiquetas).properties(
        width=760,
        height=max(180, 65 * len(resumen)),
        title=alt.TitleParams(
            text="Variación promedio de temperatura por región",
            subtitle=[
                f"n = {len(datos)} observaciones",
                f"Fuente: {fuente}",
            ],
        ),
    )
    tabla_html = resumen.rename(
        columns={
            "País__ESTANDAR": "Región",
            "promedio": "Variación promedio (°C)",
            "n": "Observaciones",
        }
    ).to_html(
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
  <p>Las barras horizontales comparan las medias entre regiones; ordenarlas de mayor a menor facilita identificar el ranking. Las cifras resumen observaciones, sin implicar causalidad.</p>
  <h2>Datos usados para el gráfico</h2>
  <p>Fuente: {fuente}. La tabla muestra el promedio y el número de observaciones que contribuyen a cada barra.</p>
  {tabla_html}
</section>
<style>
  body {{ font-family: sans-serif; margin: 2rem; }}
  .detalle {{ max-width: 900px; margin: 2rem auto; line-height: 1.5; }}
  .tabla-datos {{ border-collapse: collapse; width: 100%; }}
  .tabla-datos th, .tabla-datos td {{ border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: right; }}
  .tabla-datos th {{ background: #f2f2f2; }}
</style>
"""
    pagina = pagina.replace("</body>", f"{seccion}</body>")

    ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVO_SALIDA.write_text(pagina, encoding="utf-8")
    print("Promedio de value por región (°C):")
    print(resumen.to_string(index=False))
    print(f"\nGráfico guardado en: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    main()
