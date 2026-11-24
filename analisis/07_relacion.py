from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
ARCHIVO_ENTRADA = RAIZ_PROYECTO / "datos" / "crudo" / "datos.xlsx"
ARCHIVO_SALIDA = RAIZ_PROYECTO / "docs" / "graficos" / "relacion.html"
COLUMNAS_REQUERIDAS = ["Años__ESTANDAR", "value"]
REGION = "País__ESTANDAR"


def main():
    if not ARCHIVO_ENTRADA.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {ARCHIVO_ENTRADA}")

    datos = pd.read_excel(ARCHIVO_ENTRADA)
    faltantes_columnas = [
        columna
        for columna in [*COLUMNAS_REQUERIDAS, REGION]
        if columna not in datos.columns
    ]
    if faltantes_columnas:
        raise ValueError(f"Faltan columnas necesarias: {faltantes_columnas}")
    if datos[[*COLUMNAS_REQUERIDAS, REGION]].isna().any().any():
        raise ValueError("Hay valores faltantes en año, variación o región.")
    if datos.empty:
        raise ValueError("El archivo de entrada no contiene observaciones.")

    for columna in COLUMNAS_REQUERIDAS:
        datos[columna] = pd.to_numeric(datos[columna], errors="raise")
    if (
        datos["Años__ESTANDAR"].nunique() < 2
        or datos["value"].nunique() < 2
    ):
        raise ValueError("Se necesitan al menos dos valores distintos en ambas variables.")

    correlacion = float(
        datos["Años__ESTANDAR"].corr(datos["value"], method="pearson")
    )
    if pd.isna(correlacion):
        raise ValueError("No se pudo calcular la correlación de Pearson.")

    if correlacion > 0:
        direccion = "positiva"
    elif correlacion < 0:
        direccion = "negativa"
    else:
        direccion = "nula"
    explicacion = (
        f"El coeficiente de correlación de Pearson es r = {correlacion:.6f}. "
        f"Su signo indica una asociación lineal global {direccion} entre el año y "
        "value. La magnitud |r| indica qué tan cerca está la "
        "asociación lineal de ser perfecta: cuanto más próxima a 1, más fuerte; "
        "cuanto más próxima a 0, más débil. El coeficiente resume las observaciones "
        "de todas las regiones en conjunto; describe asociación, no causalidad."
    )

    fuente = "FAOSTAT"
    puntos = (
        alt.Chart(datos)
        .mark_circle(size=65, opacity=0.65, color="#4C78A8")
        .encode(
            x=alt.X(
                "Años__ESTANDAR:Q",
                title="Año",
                axis=alt.Axis(format="d", tickMinStep=1),
            ),
            y=alt.Y(
                "value:Q",
                title="Variación de temperatura media (°C)",
            ),
            tooltip=[
                alt.Tooltip("Años__ESTANDAR:Q", title="Año", format="d"),
                alt.Tooltip(
                    "value:Q",
                    title="Variación (°C)",
                    format=".3f",
                ),
                alt.Tooltip(f"{REGION}:N", title="Región"),
            ],
        )
    )
    tendencia = (
        alt.Chart(datos)
        .transform_regression("Años__ESTANDAR", "value")
        .mark_line(color="#E45756", strokeWidth=3)
        .encode(
            x=alt.X("Años__ESTANDAR:Q"),
            y=alt.Y("value:Q"),
        )
    )
    grafico = alt.layer(puntos, tendencia).properties(
        width=850,
        height=470,
        title=alt.TitleParams(
            text="Relación entre el año y la variación de temperatura",
            subtitle=[
                f"n = {len(datos)} observaciones · Pearson r = {correlacion:.6f}",
                f"Fuente: {fuente}",
            ],
        ),
    )

    tabla = datos[[*COLUMNAS_REQUERIDAS, REGION]].sort_values(
        ["Años__ESTANDAR", REGION]
    ).rename(
        columns={
            "Años__ESTANDAR": "Año",
            REGION: "Región",
            "value": "Variación de temperatura (°C)",
        }
    )
    tabla_html = tabla.to_html(
        index=False,
        border=0,
        classes="tabla-datos",
        table_id="datos-grafico",
        float_format=lambda valor: format(valor, ".15g"),
    )
    pagina = grafico.to_html()
    bloque_explicacion = f"""
<section class="interpretacion">
  <h2>Por qué es adecuado</h2>
  <p>El diagrama de dispersión muestra las observaciones de dos variables numéricas y su dispersión; la línea de tendencia lineal resume el patrón conjunto observado. No permite concluir causalidad.</p>
  <h2>Interpretación del coeficiente</h2>
  <p>{explicacion}</p>
  <h2>Datos usados para el gráfico</h2>
  <p>Fuente: {fuente}. La tabla incluye las observaciones representadas.</p>
  {tabla_html}
</section>
<style>
  body {{ font-family: sans-serif; margin: 2rem; }}
  .interpretacion {{ max-width: 1000px; margin: 2rem auto; line-height: 1.6; }}
  .tabla-datos {{ border-collapse: collapse; width: 100%; }}
  .tabla-datos th, .tabla-datos td {{ border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: right; }}
  .tabla-datos th {{ position: sticky; top: 0; background: #f2f2f2; }}
</style>
"""
    pagina = pagina.replace("</body>", f"{bloque_explicacion}</body>")

    ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVO_SALIDA.write_text(pagina, encoding="utf-8")
    print(f"Correlación de Pearson global: r = {correlacion:.12f}")
    print(explicacion)
    print(f"\nGráfico guardado en: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    main()
