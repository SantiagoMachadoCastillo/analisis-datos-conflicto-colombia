from decimal import Decimal, ROUND_FLOOR
from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
ARCHIVO_ENTRADA = RAIZ_PROYECTO / "datos" / "crudo" / "datos.xlsx"
ARCHIVO_SALIDA = RAIZ_PROYECTO / "docs" / "graficos" / "distribucion.html"
VARIABLE = "value"
ANCHO_INTERVALO = Decimal("0.1")


def indice_intervalo(valor):
    return int(
        (Decimal(str(valor)) / ANCHO_INTERVALO).to_integral_value(
            rounding=ROUND_FLOOR
        )
    )


def formato_limite(indice):
    return format(ANCHO_INTERVALO * indice, ".1f")


def main():
    if not ARCHIVO_ENTRADA.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {ARCHIVO_ENTRADA}")

    datos = pd.read_excel(ARCHIVO_ENTRADA)
    if VARIABLE not in datos.columns:
        raise ValueError(f"No se encontró la variable requerida: {VARIABLE}")
    if datos[VARIABLE].isna().any():
        raise ValueError(f"La variable {VARIABLE} contiene valores faltantes.")
    if datos.empty:
        raise ValueError("El archivo de entrada no contiene observaciones.")

    datos[VARIABLE] = pd.to_numeric(datos[VARIABLE], errors="raise")
    datos["indice_intervalo"] = datos[VARIABLE].map(indice_intervalo)
    primero = int(datos["indice_intervalo"].min())
    ultimo = int(datos["indice_intervalo"].max())
    frecuencias = (
        datos["indice_intervalo"]
        .value_counts()
        .reindex(range(primero, ultimo + 1), fill_value=0)
        .rename_axis("indice")
        .rename("frecuencia")
        .reset_index()
    )
    frecuencias["inicio"] = frecuencias["indice"].map(
        lambda indice: float(ANCHO_INTERVALO * int(indice))
    )
    frecuencias["fin"] = frecuencias["indice"].map(
        lambda indice: float(ANCHO_INTERVALO * (int(indice) + 1))
    )
    frecuencias["intervalo"] = frecuencias["indice"].map(
        lambda indice: (
            f"[{formato_limite(int(indice))}, "
            f"{formato_limite(int(indice) + 1)})"
        )
    )
    if int(frecuencias["frecuencia"].sum()) != len(datos):
        raise ValueError("Las frecuencias no suman el tamaño de muestra.")

    n = len(datos)
    fuente = "FAOSTAT"
    grafico = (
        alt.Chart(frecuencias)
        .mark_bar(color="#4C78A8")
        .encode(
            x=alt.X(
                "inicio:Q",
                title="Variación de temperatura media (°C)",
                scale=alt.Scale(domain=[frecuencias["inicio"].min(), frecuencias["fin"].max()]),
                axis=alt.Axis(format=".1f"),
            ),
            x2="fin:Q",
            y=alt.Y("frecuencia:Q", title="Frecuencia (observaciones)", scale=alt.Scale(zero=True)),
            tooltip=[
                alt.Tooltip("intervalo:N", title="Intervalo (°C)"),
                alt.Tooltip("frecuencia:Q", title="Frecuencia"),
            ],
        )
        .properties(
            width=800,
            height=440,
            title=alt.TitleParams(
                text="Distribución de las variaciones de temperatura",
                subtitle=[
                    f"n = {n} observaciones · intervalos de 0,1 °C",
                    f"Fuente: {fuente}",
                ],
            ),
        )
    )

    tabla_html = frecuencias[["intervalo", "frecuencia"]].rename(columns={
        "intervalo": "Intervalo de value (°C)",
        "frecuencia": "Frecuencia",
    }).to_html(
        index=False,
        border=0,
        classes="tabla-frecuencias",
        table_id="tabla-frecuencias",
    )
    pagina = grafico.to_html()
    bloque_tabla = f"""
<section class="frecuencias">
  <h2>Por qué es adecuado</h2>
  <p>Un histograma agrupa una variable numérica continua en intervalos y muestra cuántas observaciones caen en cada uno; así permite observar la forma de la distribución. No se excluyeron valores.</p>
  <h2>Frecuencias por intervalo</h2>
  <p>Ancho de intervalo: 0,1 °C. Los intervalos son cerrados por la izquierda y abiertos por la derecha: [límite inferior, límite superior).</p>
  <p>Fuente: {fuente}.</p>
  {tabla_html}
</section>
<style>
  body {{ font-family: sans-serif; margin: 2rem; }}
  .frecuencias {{ max-width: 800px; margin: 2rem auto; }}
  .tabla-frecuencias {{ border-collapse: collapse; width: 100%; }}
  .tabla-frecuencias th, .tabla-frecuencias td {{ border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: right; }}
  .tabla-frecuencias th {{ background: #f2f2f2; }}
</style>
"""
    pagina = pagina.replace("</body>", f"{bloque_tabla}</body>")

    ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVO_SALIDA.write_text(pagina, encoding="utf-8")
    print(f"n = {n}; ancho de intervalo = 0,1 °C")
    print("Frecuencias por intervalo:")
    print(frecuencias[["intervalo", "frecuencia"]].to_string(index=False))
    print(f"\nHistograma y tabla guardados en: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    main()
