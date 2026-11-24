from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
ARCHIVO_ENTRADA = RAIZ_PROYECTO / "datos" / "limpio" / "temperatura_limpia.csv"
ARCHIVO_SALIDA = RAIZ_PROYECTO / "docs" / "graficos" / "cambio_tiempo.html"
COLUMNAS_REQUERIDAS = ["anio", "variacion_temperatura", "region"]


def main():
    if not ARCHIVO_ENTRADA.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {ARCHIVO_ENTRADA}")

    datos = pd.read_csv(ARCHIVO_ENTRADA)
    faltantes_columnas = [columna for columna in COLUMNAS_REQUERIDAS if columna not in datos]
    if faltantes_columnas:
        raise ValueError(f"Faltan columnas necesarias: {faltantes_columnas}")
    if datos[COLUMNAS_REQUERIDAS].isna().any().any():
        raise ValueError("Hay valores faltantes en año, variación o región.")

    datos["anio"] = pd.to_numeric(datos["anio"], errors="raise")
    datos["variacion_temperatura"] = pd.to_numeric(
        datos["variacion_temperatura"], errors="raise"
    )
    if datos.duplicated(["anio", "region"]).any():
        raise ValueError("Hay más de una observación por año y región.")

    regiones = datos["region"].drop_duplicates().tolist()
    tabla = (
        datos.pivot(
            index="anio",
            columns="region",
            values="variacion_temperatura",
        )
        .reindex(columns=regiones)
        .reset_index()
        .rename_axis(columns=None)
        .sort_values("anio")
    )
    tabla["anio"] = tabla["anio"].astype(int)

    titulo = (
        "Evolución de la variación de la temperatura media en América Latina "
        "(1961–2025)"
    )
    fuente = "Fuente: datos/limpio/temperatura_limpia.csv."
    grafico = (
        alt.Chart(datos)
        .mark_line(point=True)
        .encode(
            x=alt.X("anio:Q", title="Año", axis=alt.Axis(format="d", tickMinStep=1)),
            y=alt.Y("variacion_temperatura:Q", title="Variación de temperatura media (°C)"),
            color=alt.Color("region:N", title="Región", sort=regiones),
            tooltip=[
                alt.Tooltip("region:N", title="Región"),
                alt.Tooltip("anio:Q", title="Año", format="d"),
                alt.Tooltip(
                    "variacion_temperatura:Q",
                    title="Variación (°C)",
                    format=".3f",
                ),
            ],
        )
        .properties(
            width=850,
            height=460,
            title=alt.TitleParams(
                text=titulo,
                subtitle=[f"n = {len(datos)} observaciones", fuente],
            ),
        )
        .interactive()
    )

    tabla_html = tabla.to_html(
        index=False,
        border=0,
        na_rep="Sin dato",
        classes="tabla-cifras",
        formatters={
            region: lambda valor: format(valor, ".15g") if pd.notna(valor) else "Sin dato"
            for region in regiones
        },
        table_id="cifras-anuales",
    )
    pagina = grafico.to_html()
    bloque_tabla = f"""
<section class="datos-exactos">
  <h2>Cifras anuales exactas</h2>
  <p>Valores de variación por año y región, tal como se leen del CSV de entrada.</p>
  {tabla_html}
</section>
<style>
  body {{ font-family: sans-serif; margin: 2rem; }}
  .datos-exactos {{ max-width: 1000px; margin: 2rem auto; }}
  .tabla-cifras {{ border-collapse: collapse; width: 100%; }}
  .tabla-cifras th, .tabla-cifras td {{ border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: right; }}
  .tabla-cifras th {{ position: sticky; top: 0; background: #f2f2f2; }}
</style>
"""
    pagina = pagina.replace("</body>", f"{bloque_tabla}</body>")

    ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVO_SALIDA.write_text(pagina, encoding="utf-8")
    print(f"Observaciones representadas: {len(datos)}")
    print(f"Regiones: {', '.join(regiones)}")
    print(f"Años: {int(datos['anio'].min())}–{int(datos['anio'].max())}")
    print(f"Gráfico y tabla guardados en: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    main()
