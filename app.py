import os
import sys
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify

# Importación de los 5 módulos temáticos independientes
from glosario import obtener_terminos, obtener_estadisticas_glosario
from linea_tiempo import obtener_hitos
from clasificacion import obtener_clasificacion, obtener_niveles_funcionales
from machine_learning import obtener_info_ml, clasificar_mensaje_spam
from ensayo import obtener_ensayo

app = Flask(__name__)

# Configuración básica
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    """
    Ruta principal que renderiza la aplicación web con todos sus módulos integrados.
    Permite filtrar el glosario y seleccionar la sección activa mediante parámetros GET.
    """
    query = request.args.get('q', '').strip()
    nivel_filtro = request.args.get('nivel', '').strip()
    seccion_activa = request.args.get('sec', 'glosario').strip().lower()

    # Si se realizó una búsqueda en el glosario, aseguramos que la sección activa sea glosario
    if query or nivel_filtro:
        seccion_activa = 'glosario'

    # Datos del Glosario
    terminos_filtrados = obtener_terminos(query=query, nivel_filtro=nivel_filtro)
    stats_glosario = obtener_estadisticas_glosario()

    # Datos de la Línea de Tiempo
    hitos_timeline = obtener_hitos()

    # Datos de Clasificación
    clasificacion_ia = obtener_clasificacion()
    niveles_funcionales = obtener_niveles_funcionales()

    # Datos de Machine Learning
    ml_info = obtener_info_ml()

    # Datos del Ensayo Académico
    ensayo_info = obtener_ensayo()

    return render_template(
        'index.html',
        # Parámetros de navegación y filtros
        seccion_activa=seccion_activa,
        query=query,
        nivel_actual=nivel_filtro,
        # Glosario
        terminos=terminos_filtrados,
        total_terminos=len(terminos_filtrados),
        stats_glosario=stats_glosario,
        # Línea de Tiempo
        hitos=hitos_timeline,
        # Clasificación
        clasificacion=clasificacion_ia,
        niveles_funcionales=niveles_funcionales,
        # Machine Learning
        ml_info=ml_info,
        # Ensayo
        ensayo=ensayo_info
    )

@app.route('/api/ml/predict', methods=['POST', 'GET'])
def api_predict_spam():
    """
    API endpoint para el modelo interactivo de Machine Learning.
    Recibe un texto y devuelve el diagnóstico en tiempo real en formato JSON.
    """
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        texto = data.get('texto', '').strip()
    else:
        texto = request.args.get('texto', '').strip()

    if not texto:
        return jsonify({
            "error": True,
            "mensaje": "Por favor proporciona un texto válido para clasificar."
        }), 400

    resultado = clasificar_mensaje_spam(texto)
    return jsonify(resultado)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    print("=" * 60)
    print(" INICIANDO SERVIDOR WEB DE INTELIGENCIA ARTIFICIAL (FLASK)")
    print(" Modulos cargados:")
    print("  [*] glosario.py           -> 20 Conceptos tecnicos con filtros")
    print("  [*] linea_tiempo.py       -> 10 Hitos historicos y curiosidades")
    print("  [*] clasificacion.py      -> Clasificacion de IA (Debil, Fuerte, ASI)")
    print("  [*] machine_learning.py   -> Teoria + Ejemplo interactivo Naive Bayes")
    print("  [*] ensayo.py             -> Ensayo de Etica y aspectos sociales de la IA")
    print(" Servidor disponible en: http://127.0.0.1:5000/")
    print("=" * 60)
    Timer(1.2, open_browser).start()
    app.run(host='127.0.0.1', port=5000, debug=False)
