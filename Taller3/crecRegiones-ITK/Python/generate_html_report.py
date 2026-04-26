"""
Generates an HTML report with embedded images (base64) so it's a single
self-contained file that can be opened in any browser or imported into
Google Docs / Word.
"""
import base64
import os

REPORT_DIR = ".."
IMG_DIR = os.path.join(REPORT_DIR, "resultados_png")
OUTPUT = os.path.join(REPORT_DIR, "INFORME_Segmentacion.html")

def img_b64(filename):
    path = os.path.join(IMG_DIR, filename)
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/png;base64,{data}" style="max-width:100%; border:1px solid #ccc; margin:10px 0;">'

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Informe - Segmentación por Crecimiento de Regiones con ITK</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #222; line-height: 1.6; }}
  h1 {{ color: #1a5276; border-bottom: 3px solid #1a5276; padding-bottom: 10px; }}
  h2 {{ color: #2c3e50; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 40px; }}
  h3 {{ color: #34495e; }}
  h4 {{ color: #555; }}
  table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
  th, td {{ border: 1px solid #ccc; padding: 8px 12px; text-align: left; }}
  th {{ background: #2c3e50; color: white; }}
  tr:nth-child(even) {{ background: #f9f9f9; }}
  code, pre {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
  pre {{ padding: 12px; overflow-x: auto; }}
  .obs {{ background: #eaf2f8; border-left: 4px solid #2980b9; padding: 10px 15px; margin: 10px 0; }}
  .conclusion {{ background: #e8f8f5; border-left: 4px solid #1abc9c; padding: 15px; margin: 20px 0; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 30px 0; }}
</style>
</head>
<body>

<h1>Informe: Segmentación por Crecimiento de Regiones con ITK</h1>

<h2>1. Objetivo</h2>
<p>Segmentar los ventrículos cerebrales en un volumen de resonancia magnética (RM) ponderada en T1 utilizando dos técnicas de crecimiento de regiones implementadas con la librería ITK (Insight Toolkit):</p>
<ol>
  <li><strong>ConnectedThreshold</strong> — umbrales manuales definidos por el usuario.</li>
  <li><strong>ConfidenceConnected</strong> — umbrales automáticos calculados estadísticamente.</li>
</ol>
<p>Se busca comparar ambos métodos variando sus parámetros para evaluar la calidad de la segmentación y su sensibilidad a la configuración.</p>

<hr>

<h2>2. Imagen de Entrada</h2>
<ul>
  <li><strong>Archivo:</strong> <code>A1_grayT1.nii</code> / <code>A1_grayT1.nii.gz</code></li>
  <li><strong>Tipo:</strong> Volumen 3D de resonancia magnética cerebral ponderada en T1, escala de grises.</li>
  <li><strong>Dimensiones:</strong> 288 × 320 × 208 vóxeles.</li>
  <li><strong>Características T1:</strong> La sustancia blanca aparece clara (intensidad alta), la sustancia gris en tonos intermedios, y el líquido cefalorraquídeo (LCR) — incluyendo los ventrículos — aparece oscuro (intensidad baja). Esto hace que los ventrículos sean un buen candidato para segmentación por crecimiento de regiones.</li>
</ul>
<p><strong>Semilla utilizada en todos los experimentos:</strong> (132, 142, 96) — punto ubicado dentro del ventrículo lateral.</p>

<hr>

<h2>3. Descripción de los Métodos</h2>

<h3>3.1 ConnectedThreshold (Umbrales Manuales)</h3>
<p>Este método parte de un punto semilla y examina los vóxeles vecinos. Si la intensidad de un vecino está dentro del rango [Lower, Upper] definido por el usuario, se agrega a la región segmentada. El proceso se repite hasta que no quedan más vecinos que cumplan el criterio.</p>

<table>
  <tr><th>Parámetro</th><th>Descripción</th></tr>
  <tr><td><code>LowerThreshold</code></td><td>Umbral inferior de intensidad</td></tr>
  <tr><td><code>UpperThreshold</code></td><td>Umbral superior de intensidad</td></tr>
  <tr><td><code>XSeed, YSeed, ZSeed</code></td><td>Coordenadas de la semilla</td></tr>
</table>

<p><strong>Ejecución:</strong></p>
<pre>python3 ConnectedThreshold.py A1_grayT1.nii.gz output.nii.gz 100 170 132 142 96</pre>

<p><strong>Ventaja:</strong> Control total sobre el rango de intensidad.<br>
<strong>Desventaja:</strong> Requiere conocimiento previo de las intensidades de la estructura objetivo.</p>

<h3>3.2 ConfidenceConnected (Umbrales Automáticos)</h3>
<p>También es crecimiento de regiones, pero los umbrales se calculan automáticamente. El algoritmo toma el vecindario alrededor de la semilla, calcula la media (μ) y desviación estándar (σ), y define el rango como <strong>[μ − f·σ, μ + f·σ]</strong>, donde f es el multiplicador. Opcionalmente puede iterar: después de segmentar, recalcula μ y σ con los vóxeles ya incluidos y vuelve a crecer.</p>

<table>
  <tr><th>Parámetro</th><th>Descripción</th></tr>
  <tr><td><code>NumberOfIterations</code></td><td>Veces que recalcula estadísticas y re-crece (0 = una pasada)</td></tr>
  <tr><td><code>Multiplier</code></td><td>Factor f que multiplica σ. Mayor = más permisivo</td></tr>
  <tr><td><code>InitialNeighborhoodRadius</code></td><td>Radio del vecindario para estadísticas iniciales (ej: 1 = cubo 3×3×3)</td></tr>
  <tr><td><code>XSeed, YSeed, ZSeed</code></td><td>Coordenadas de la semilla</td></tr>
</table>

<p><strong>Ejecución:</strong></p>
<pre>python3 ConfidenceConnected.py A1_grayT1.nii.gz output.nii.gz 0 2 1 132 142 96</pre>

<p><strong>Ventaja:</strong> No requiere adivinar los umbrales; se adapta a la intensidad local.<br>
<strong>Desventaja:</strong> Depende de que la semilla esté en una zona representativa.</p>

<hr>

<h2>4. Experimentos y Resultados</h2>

<h3>4.1 ConnectedThreshold — Variación de Umbrales</h3>

<h4>Comparación general (corte axial)</h4>
{img_b64("comparacion_ConnectedThreshold.png")}

<h4>Prueba 1: Rango restrictivo — Lower=80, Upper=140</h4>
{img_b64("CT_narrow_80_140.png")}
<div class="obs"><strong>Parámetros:</strong> Lower=80, Upper=140<br>
<strong>Observación:</strong> La segmentación es muy conservadora. Solo captura una porción pequeña del ventrículo. El rango es demasiado estrecho y excluye vóxeles que sí pertenecen a la estructura. Archivo de salida: 37 KB.</div>

<h4>Prueba 2: Rango por defecto — Lower=100, Upper=170</h4>
{img_b64("CT_default_100_170.png")}
<div class="obs"><strong>Parámetros:</strong> Lower=100, Upper=170<br>
<strong>Observación:</strong> Buena segmentación del ventrículo. El rango captura la mayor parte de la estructura ventricular sin desbordarse significativamente. Este es el balance más adecuado. Archivo: 68 KB.</div>

<h4>Prueba 3: Rango amplio — Lower=60, Upper=200</h4>
{img_b64("CT_wide_60_200.png")}
<div class="obs"><strong>Parámetros:</strong> Lower=60, Upper=200<br>
<strong>Observación:</strong> La segmentación se desborda considerablemente, incluyendo tejido que no pertenece al ventrículo. Archivo: 807 KB.</div>

<h4>Prueba 4: Rango muy amplio — Lower=50, Upper=250</h4>
{img_b64("CT_verywide_50_250.png")}
<div class="obs"><strong>Parámetros:</strong> Lower=50, Upper=250<br>
<strong>Observación:</strong> Desbordamiento severo. La segmentación invade gran parte del cerebro. Demuestra la importancia de elegir umbrales adecuados. Archivo: 1.0 MB.</div>

<hr>

<h3>4.2 ConfidenceConnected — Variación de Parámetros Estadísticos</h3>

<h4>Comparación general (corte axial)</h4>
{img_b64("comparacion_ConfidenceConnected.png")}

<h4>Prueba 1: Conservador — Mult=1, Iter=0, Rad=1</h4>
{img_b64("CC_m1_i0_r1.png")}
<div class="obs"><strong>Parámetros:</strong> Multiplier=1, Iterations=0, Radius=1<br>
<strong>Observación:</strong> Segmentación conservadora. Con multiplicador 1 (rango μ ± 1σ), solo se incluyen vóxeles muy similares a la semilla. Captura el ventrículo de forma contenida. Archivo: 41 KB.</div>

<h4>Prueba 2: Default — Mult=2, Iter=0, Rad=1</h4>
{img_b64("CC_m2_i0_r1.png")}
<div class="obs"><strong>Parámetros:</strong> Multiplier=2, Iterations=0, Radius=1<br>
<strong>Observación:</strong> Con multiplicador 2 (μ ± 2σ) el rango es más amplio pero la estructura del ventrículo se mantiene bien delimitada. Buen punto de partida. Archivo: 41 KB.</div>

<h4>Prueba 3: Con iteraciones — Mult=2, Iter=3, Rad=1</h4>
{img_b64("CC_m2_i3_r1.png")}
<div class="obs"><strong>Parámetros:</strong> Multiplier=2, Iterations=3, Radius=1<br>
<strong>Observación:</strong> Al agregar 3 iteraciones, el algoritmo recalcula estadísticas y vuelve a crecer. El resultado es similar al anterior, sugiriendo que la región converge rápidamente. Archivo: 41 KB.</div>

<h4>Prueba 4: Agresivo — Mult=3, Iter=2, Rad=2</h4>
{img_b64("CC_m3_i2_r2.png")}
<div class="obs"><strong>Parámetros:</strong> Multiplier=3, Iterations=2, Radius=2<br>
<strong>Observación:</strong> Con multiplicador 3 y radio 2, la segmentación se desborda significativamente. Incluso el método automático puede fallar con parámetros agresivos. Archivo: 1.0 MB.</div>

<hr>

<h2>5. Comparación de Métodos</h2>

<table>
  <tr><th>Aspecto</th><th>ConnectedThreshold</th><th>ConfidenceConnected</th></tr>
  <tr><td><strong>Tipo de umbral</strong></td><td>Manual (usuario define Lower/Upper)</td><td>Automático (calculado con μ ± f·σ)</td></tr>
  <tr><td><strong>Facilidad de uso</strong></td><td>Requiere conocer las intensidades</td><td>Solo requiere semilla y multiplicador</td></tr>
  <tr><td><strong>Sensibilidad</strong></td><td>Muy sensible al rango elegido</td><td>Más robusto con parámetros moderados</td></tr>
  <tr><td><strong>Mejor resultado</strong></td><td>Lower=100, Upper=170</td><td>Mult=2, Iter=0-3, Rad=1</td></tr>
  <tr><td><strong>Riesgo de desbordamiento</strong></td><td>Alto con rangos amplios</td><td>Menor con multiplicadores bajos</td></tr>
  <tr><td><strong>Adaptabilidad</strong></td><td>No se adapta a variaciones locales</td><td>Se adapta a la estadística local</td></tr>
</table>

<div class="conclusion">
<strong>Conclusión:</strong> ConfidenceConnected es más robusto y fácil de usar para segmentar ventrículos, ya que calcula los umbrales automáticamente y es menos sensible a la elección de parámetros (siempre que el multiplicador sea razonable, entre 1 y 2.5). ConnectedThreshold ofrece más control pero requiere experimentación manual para encontrar el rango correcto, y es más propenso a desbordamiento con rangos amplios.
</div>

<hr>

<h2>6. Visor Interactivo</h2>
<p>Además de los scripts originales, se desarrolló un <strong>visor interactivo</strong> (<code>interactive_segmentation.py</code>) que permite:</p>
<ul>
  <li>Visualizar el volumen original en cortes axial, coronal y sagital.</li>
  <li>Cambiar entre ambos métodos con radio buttons.</li>
  <li>Ajustar todos los parámetros en tiempo real con sliders.</li>
  <li>Ejecutar la segmentación y ver el resultado superpuesto sobre la imagen original.</li>
  <li>Visualizar la posición de la semilla con un marcador verde.</li>
</ul>
<p><strong>Ejecución:</strong></p>
<pre>python3 interactive_segmentation.py A1_grayT1.nii.gz</pre>

<hr>

<h2>7. Archivos del Proyecto</h2>
<table>
  <tr><th>Archivo</th><th>Descripción</th></tr>
  <tr><td><code>A1_grayT1.nii.gz</code></td><td>Volumen RM T1 de cerebro (entrada)</td></tr>
  <tr><td><code>ConnectedThreshold.py</code></td><td>Segmentación con umbrales manuales</td></tr>
  <tr><td><code>ConfidenceConnected.py</code></td><td>Segmentación con umbrales automáticos</td></tr>
  <tr><td><code>interactive_segmentation.py</code></td><td>Visor interactivo con ambos métodos</td></tr>
  <tr><td><code>generate_comparison_images.py</code></td><td>Generador de imágenes PNG comparativas</td></tr>
  <tr><td><code>resultados_png/</code></td><td>Carpeta con todas las imágenes de resultados</td></tr>
</table>
<p><strong>Requisitos:</strong> Python 3, ITK (<code>pip install itk</code>), matplotlib, numpy.</p>

</body>
</html>
"""

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Report saved to: {OUTPUT}")
