import json
import os
import socket
import sys
import unicodedata
import urllib.error
import urllib.request
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify

# Importación de los 5 módulos temáticos independientes
from glosario import obtener_terminos, obtener_estadisticas_glosario
from linea_tiempo import obtener_hitos
from clasificacion import obtener_clasificacion, obtener_niveles_funcionales
from machine_learning import obtener_info_ml, clasificar_mensaje_spam
from ensayo import obtener_ensayo
from algoritmo import obtener_info_algoritmos, obtener_infografia

app = Flask(__name__)

# Configuración básica
app.config['JSON_AS_ASCII'] = False

# --- Clasificador ML for Kids (integrado en el portal) ---------------------

# API key por defecto del usuario. Se puede editar desde la misma pantalla
# sin necesidad de pasos previos de conexión ni recargas.
ML4K_API_KEY_DEFAULT = "4df1f280-d8b8-11f1-9dd6-979fe2bdb61c21a47247-91c5-4685-a78b-af78ee870c43"

CLASS_TYPES = {"evolutiva", "heuristica", "ciega", "desconocida"}


def _norm_ml4k(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFD", texto or "").encode("ascii", "ignore").decode()
    return sin_tildes.strip().lower()


def tipo_algoritmo_ml4k(class_name: str) -> str:
    tipo = _norm_ml4k(class_name)
    return tipo if tipo in CLASS_TYPES else "desconocida"


def nivel_confianza_ml4k(confidence: float) -> str:
    if confidence >= 70:
        return "alta"
    if confidence >= 50:
        return "media"
    return "baja"


def url_ml4k(api_key: str, endpoint: str) -> str:
    return f"https://machinelearningforkids.co.uk/api/scratch/{api_key}/{endpoint}"

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

    # Datos de Algoritmos de Búsqueda (módulo algoritmo.py)
    info_algoritmos = obtener_info_algoritmos()
    infografia_busqueda = obtener_infografia()

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
        ensayo=ensayo_info,
        # Algoritmos de Búsqueda
        info_algoritmos=info_algoritmos,
        infografia_busqueda=infografia_busqueda
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

@app.route('/api/clasificador-ml4k/classify', methods=['POST'])
def api_clasificar_ml4k():
    """
    Clasifica un texto mediante el modelo entrenado en Machine Learning for Kids.
    Recibe el texto y usa la API key enviada en la cabecera X-API-Key (o la
    API key por defecto del portal).
    """
    api_key = request.headers.get("X-API-Key") or request.args.get("api_key") or ML4K_API_KEY_DEFAULT
    if not api_key:
        return jsonify({"error": "Ingresa una API key de Machine Learning for Kids"}), 400

    data = request.get_json(silent=True) or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({"error": "Texto vacío"}), 400

    try:
        payload = json.dumps({"data": text}).encode("utf-8")
        req = urllib.request.Request(
            url_ml4k(api_key, "classify"),
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
        if not response_data:
            return jsonify({"error": "No se detectó ninguna clase"}), 404

        classifications = sorted(response_data, key=lambda x: x.get('confidence', 0), reverse=True)
        for cls in classifications:
            conf = round(float(cls.get('confidence', 0)), 1)
            cls['confidence'] = conf
            cls['algorithm_type'] = tipo_algoritmo_ml4k(cls.get('class_name'))
            cls['confidence_pct'] = f"{conf:g}%"
            cls['confidence_level'] = nivel_confianza_ml4k(conf)

        return jsonify({
            "classifications": classifications,
            "top_result": classifications[0]
        })
    except urllib.error.HTTPError as err:
        return jsonify({"error": f"Error del modelo (código {err.code}). ¿Está entrenado?"}), err.code
    except urllib.error.URLError as err:
        if isinstance(err.reason, socket.timeout):
            return jsonify({"error": "Timeout: el modelo tardó demasiado en responder"}), 504
        return jsonify({"error": str(err)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/clasificador-ml4k/status', methods=['GET'])
def api_estado_ml4k():
    """
    Devuelve el estado de entrenamiento del modelo ML for Kids asociado a la
    API key enviada (cabecera X-API-Key, parámetro api_key o valor por defecto).
    """
    api_key = request.headers.get("X-API-Key") or request.args.get("api_key") or ML4K_API_KEY_DEFAULT
    if not api_key:
        return jsonify({"status": 0, "msg": "Ingresa tu API key de ML for Kids", "type": "text"})
    try:
        with urllib.request.urlopen(url_ml4k(api_key, "status"), timeout=10) as resp:
            return jsonify(json.loads(resp.read().decode("utf-8")))
    except urllib.error.HTTPError as err:
        return jsonify({"status": 0, "msg": f"Error: {err.code} - Modelo no encontrado o no entrenado", "type": "text"}), 200
    except urllib.error.URLError as err:
        return jsonify({"status": 0, "msg": str(err), "type": "text"}), 200
    except Exception as e:
        return jsonify({"status": 0, "msg": str(e), "type": "text"})


@app.route('/ensayo/imprimir')
def ensayo_imprimir():
    """
    Vista de impresión del ensayo: documento A4 independiente (portada con los
    datos del curso, índice, resumen, secciones y referencias) renderizado
    desde ensayo.py. Es la fuente para generar el PDF estático
    static/Ensayo_Etica_IA.pdf que se muestra incrustado en la sección de ensayo
    (regenerarlo con generar_pdf.bat).
    """
    return render_template('ensayo_pdf.html', ensayo=obtener_ensayo())

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
    print("  [*] algoritmo.py          -> Algoritmos de busqueda + Infografia interactiva")
    print("  [*] clasificador ML for Kids -> Clasificador de texto integrado en el portal")
    print(" Servidor disponible en: http://127.0.0.1:5000/")
    print("=" * 60)
    Timer(1.2, open_browser).start()
    app.run(host='127.0.0.1', port=5000, debug=False)