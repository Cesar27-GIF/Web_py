from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

import unicodedata

CLASS_TYPES = {"evolutiva", "heuristica", "ciega", "desconocida"}


def _norm(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFD", texto or "").encode("ascii", "ignore").decode()
    return sin_tildes.strip().lower()


def get_algorithm_type(class_name: str) -> str:
    tipo = _norm(class_name)
    return tipo if tipo in CLASS_TYPES else "desconocida"


def get_confidence_level(confidence: float) -> str:
    if confidence >= 70:
        return "alta"
    if confidence >= 50:
        return "media"
    return "baja"


def ml4k_url(api_key: str, endpoint: str) -> str:
    return f"https://machinelearningforkids.co.uk/api/scratch/{api_key}/{endpoint}"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clasificador ML for Kids</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #f5f5f7;
    color: #1d1d1f;
    line-height: 1.5;
    padding: 24px;
  }
  .container {
    max-width: 700px;
    margin: 0 auto;
  }
  header {
    text-align: center;
    margin-bottom: 32px;
  }
  h1 {
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.01em;
    margin-bottom: 8px;
  }
  p.subtitle {
    color: #6e6e73;
    font-size: 16px;
  }
  .card {
    background: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .card h2 {
    font-size: 15px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6e6e73;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .card h2 .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #c7c7cc;
  }
  label {
    display: block;
    font-size: 13px;
    font-weight: 500;
    color: #1d1d1f;
    margin-bottom: 6px;
  }
  input[type="password"], textarea {
    width: 100%;
    padding: 12px 14px;
    border: 1px solid #d2d2d7;
    border-radius: 8px;
    background: #ffffff;
    color: #1d1d1f;
    font-size: 15px;
    font-family: inherit;
    outline: none;
    transition: border-color 0.2s;
  }
  input[type="password"]:focus, textarea:focus {
    border-color: #1d1d1f;
  }
  textarea {
    min-height: 120px;
    resize: vertical;
  }
  .row {
    display: flex;
    gap: 12px;
    align-items: flex-end;
    margin-top: 8px;
  }
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 12px 20px;
    background: #1d1d1f;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 500;
    font-family: inherit;
    cursor: pointer;
  }
  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .msg {
    margin-top: 12px;
    font-size: 13px;
    min-height: 20px;
  }
  .msg.ok { color: #34c759; }
  .msg.error { color: #ff3b30; }
  .msg.warn { color: #ff9500; }
  .hidden { display: none; }
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
  }
  .status.ready { background: #e6f4ea; color: #34c759; }
  .status.training { background: #fdf3e2; color: #ff9500; }
  .status.error { background: #fdecea; color: #ff3b30; }
  .result {
    background: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 12px;
    padding: 24px;
    margin-top: 24px;
  }
  .result-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 16px;
  }
  .result-class {
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.02em;
  }
  .result-score {
    text-align: right;
  }
  .score-value {
    font-size: 32px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
  }
  .score-label {
    font-size: 12px;
    color: #6e6e73;
    margin-top: 2px;
  }
  .bar {
    height: 6px;
    background: #e5e5ea;
    border-radius: 3px;
    overflow: hidden;
    margin: 16px 0;
  }
  .bar > span {
    display: block;
    height: 100%;
    background: #1d1d1f;
    transition: width 0.4s ease;
  }
  .meta {
    font-size: 13px;
    color: #6e6e73;
    margin-bottom: 8px;
  }
  .all-classes {
    margin-top: 20px;
    border-top: 1px solid #e5e5ea;
    padding-top: 20px;
  }
  .all-classes h3 {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6e6e73;
    margin-bottom: 12px;
  }
  .class-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #f2f2f7;
  }
  .class-row:last-child { border-bottom: none; }
  .class-name {
    font-weight: 500;
    min-width: 120px;
  }
  .class-bar {
    flex: 1;
    height: 6px;
    background: #e5e5ea;
    border-radius: 3px;
    overflow: hidden;
  }
  .class-bar > span {
    display: block;
    height: 100%;
    background: #1d1d1f;
  }
  .class-pct {
    font-size: 13px;
    font-variant-numeric: tabular-nums;
    min-width: 40px;
    text-align: right;
  }
  .examples {
    background: #f5f5f7;
    border-radius: 12px;
    padding: 20px;
    margin-top: 24px;
  }
  .examples h3 {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6e6e73;
    margin-bottom: 12px;
  }
  .example-list {
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
  }
  .example-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 12px;
    background: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
  }
  .example-item:hover {
    border-color: #1d1d1f;
    background: #f2f2f7;
  }
  .example-tag {
    font-size: 11px;
    color: #6e6e73;
    font-weight: 500;
  }
  .footer {
    margin-top: 32px;
    font-size: 12px;
    color: #6e6e73;
    text-align: center;
  }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>Clasificador ML for Kids</h1>
    <p class="subtitle">Clasifica texto en algoritmos evolutivos, heurísticos, ciegos o desconocidos</p>
  </header>

  <!-- Todo en una sola pantalla: API key + clasificador -->
  <div class="card">
    <h2><span class="dot"></span>Configurar y clasificar</h2>

    <div>
      <label>API Key de Machine Learning for Kids</label>
      <input type="password" id="apiKeyInput" placeholder="Pega tu API key aqu&iacute;">
    </div>

    <div>
      <label>Texto a clasificar</label>
      <textarea id="texto" rows="5" placeholder="Escribe el texto que quieres clasificar..."></textarea>
    </div>

    <div class="row">
      <button class="btn" id="btnClasificar" onclick="clasificar()">
        <span id="btnTexto">Clasificar</span>
      </button>
    </div>

    <div id="msg" class="msg"></div>
  </div>

  <!-- Estado del modelo -->
  <div class="card hidden" id="modelStatus">
    <h2><span class="dot"></span>Estado del modelo</h2>
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <span id="statusBadge" class="status-badge status error">No entrenado</span>
    </div>
    <p id="statusMsg" class="msg" style="margin-top: 8px;"></p>
  </div>

  <!-- Resultados -->
  <div id="resultado"></div>

  <!-- Entrenamiento del modelo -->
  <div class="card">
    <h2><span class="dot"></span>Entrenamiento del modelo</h2>
    <p style="font-size: 14px; color: #1d1d1f; margin-bottom: 16px;">
      El modelo de Machine Learning for Kids se entrena con ejemplos de texto que tú proporcionas para cada clase (ciaga, heurística, evolutiva o desconocida). Durante el entrenamiento, el sistema aprende a reconocer patrones en las palabras y frases de cada categoría para poder clasificarlos automáticamente después.
    </p>
    <div style="font-size: 13px; color: #6e6e73;">
      <p style="margin-bottom: 8px;"><strong>Cómo funciona:</strong></p>
      <ul style="margin-left: 18px; margin-bottom: 16px;">
        <li>Recopilas ejemplos de texto para cada tipo de algoritmo.</li>
        <li>Entrenas el modelo en la plataforma de Machine Learning for Kids.</li>
        <li>El modelo guarda los patrones aprendidos en una API key única.</li>
        <li>Esta aplicación consulta ese modelo usando tu API key.</li>
      </ul>
      <p><strong>Tipos de algoritmo que detecta:</strong></p>
      <ul style="margin-left: 18px;">
        <li><strong>Ciega:</strong> explora sin saber cuán cerca está la meta (BFS, DFS, costo uniforme).</li>
        <li><strong>Heurística:</strong> usa una estimación para elegir el camino más prometedor (A*, Greedy).</li>
        <li><strong>Evolutiva:</strong> mejora una población mediante selección, cruce y mutación (algoritmos genéticos).</li>
        <li><strong>Desconocida:</strong> el texto no encaja con ninguna familia o mezcla varias.</li>
      </ul>
    </div>
  </div>

  <!-- Ejemplos -->
  <div class="examples" id="ejemplosArea">
    <h3>Ejemplos</h3>
    <div class="example-list" id="exampleGrid"></div>
  </div>

  <div class="footer">
    Los resultados provienen del modelo entrenado en Machine Learning for Kids.
  </div>
</div>

<script>
  const EJEMPLOS = [
    'Expande primero todos los nodos de un nivel antes de pasar al siguiente.',
    'Usa una estimaci&oacute;n de la distancia a la meta para elegir el camino m&aacute;s prometedor.',
    'Cruza y muta una poblaci&oacuten de soluciones durante varias generaciones.',
    'Combina una estimaci&oacute;n con feromonas que dejan los individuos.',
    'La mutaci&oacuten del virus oblig&oacute a desarrollar una nueva vacuna.'
  ];

  document.addEventListener('DOMContentLoaded', () => {
    const savedKey = localStorage.getItem('ml4k_api_key');
    if (savedKey) {
      document.getElementById('apiKeyInput').value = savedKey;
    }

    const grid = document.getElementById('exampleGrid');
    EJEMPLOS.forEach((texto, i) => {
      const item = document.createElement('div');
      item.className = 'example-item';
      item.innerHTML = `<span>${texto}</span><span class="example-tag">Ejemplo ${i + 1}</span>`;
      item.onclick = () => {
        document.getElementById('texto').value = texto;
        clasificar();
      };
      grid.appendChild(item);
    });
  });

  async function apiFetch(path, options = {}) {
    const apiKey = document.getElementById('apiKeyInput').value.trim();
    if (!apiKey) throw new Error('Ingresa una API key');

    const headers = {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey,
      ...options.headers,
    };

    const separator = path.includes('?') ? '&' : '?';
    const url = path + separator + 'api_key=' + encodeURIComponent(apiKey);
    const res = await fetch(url, { ...options, headers });
    return res.json();
  }

  async function clasificar() {
    const apiKey = document.getElementById('apiKeyInput').value.trim();
    const textInput = document.getElementById('texto').value.trim();
    const btn = document.getElementById('btnClasificar');
    const msg = document.getElementById('msg');
    const resultDiv = document.getElementById('resultado');

    if (!apiKey) {
      msg.textContent = 'Ingresa una API key';
      msg.className = 'msg error';
      return;
    }

    if (!textInput) {
      msg.textContent = 'Escribe un texto para clasificar';
      msg.className = 'msg error';
      return;
    }

    btn.disabled = true;
    btn.querySelector('span').textContent = 'Clasificando...';
    msg.textContent = '';
    resultDiv.innerHTML = '';

    try {
      localStorage.setItem('ml4k_api_key', apiKey);

      const response = await fetch('/api/classify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey,
        },
        body: JSON.stringify({ text: textInput }),
      });

      const data = await response.json();

      if (data.error) {
        mostrarError(data.error);
        return;
      }

      // Consultar estado para mostrarlo
      try {
        const statusData = await apiFetch('/api/status', { method: 'GET' });
        updateStatusUI(statusData);
      } catch (e) {
        // Silencioso
      }

      mostrarResultados(data);

    } catch (error) {
      mostrarError('Error de conexi&oacuten: ' + error.message);
    } finally {
      btn.disabled = false;
      btn.querySelector('span').textContent = 'Clasificar';
    }
  }

  async function updateStatusUI(data) {
    const statusDiv = document.getElementById('modelStatus');
    const badge = document.getElementById('statusBadge');
    const msg = document.getElementById('statusMsg');

    if (data.status === 2) {
      badge.className = 'status-badge status ready';
      badge.textContent = 'Listo';
      msg.textContent = 'El modelo est&aacute; entrenado y disponible';
    } else if (data.status === 1) {
      badge.className = 'status-badge status training';
      badge.textContent = 'Entrenando';
      msg.textContent = data.msg || 'El modelo se est&aacute; entrenando...';
    } else {
      badge.className = 'status-badge status error';
      badge.textContent = 'No entrenado';
      msg.textContent = data.msg || 'Entrena tu modelo en ML for Kids primero';
    }
    statusDiv.classList.remove('hidden');
  }

  function _norm(s) {
    return (s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  }

  function getAlgorithmColorClass(type) {
    const colors = {
      evolutiva: '#34c759',
      heuristica: '#ff9500',
      ciega: '#ff3b30',
      desconocida: '#8e8e93',
    };
    return colors[type] || '#8e8e93';
  }

  function getAlgorithmLabel(type) {
    const labels = {
      evolutiva: 'Evolutiva',
      heuristica: 'Heurística',
      ciega: 'Ciega',
      desconocida: 'Desconocida',
    };
    return labels[type] || type;
  }

  function mostrarResultados(data) {
    const resultDiv = document.getElementById('resultado');
    const results = data.classifications || [data.top_result].filter(Boolean);
    const top = data.top_result || results[0];

    if (!top) {
      resultDiv.innerHTML = '<div class="card"><div class="msg error" style="padding: 16px;">No se obtuvieron resultados.</div></div>';
      return;
    }

    const conf = top.confidence || 0;
    const nivel = conf >= 70 ? 'alta' : (conf >= 50 ? 'media' : 'baja');

    let html = '<div class="card result">';
    html += '<div class="result-header">';
    html += '<div>';
    html += '<div class="result-class">' + top.class_name + '</div>';
    html += '<div class="meta">Confianza: <strong>' + nivel + '</strong></div>';
    html += '</div>';
    html += '<div class="result-score">';
    html += '<div class="score-value">' + conf + '%</div>';
    html += '<div class="score-label">Puntuaci&oacute;n</div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="bar"><span style="width: ' + conf + '%; background: ' + getAlgorithmColorClass(_norm(top.class_name)) + '"></span></div>';
    html += '</div>';

    if (results.length > 1) {
      html += '<div class="all-classes">';
      html += '<h3>Todas las clasificaciones</h3>';
      html += '<div style="display: flex; flex-direction: column; gap: 8px;">';
      results.forEach((cls, i) => {
        const c = cls.confidence || 0;
        const esTop = i === 0;
        html += '<div class="class-row' + (esTop ? ' result-top' : '') + '">';
        html += '<span class="class-name' + (esTop ? ' font-bold' : '') + '">' + cls.class_name + '</span>';
        html += '<div class="class-bar"><span style="width: ' + c + '%; background: ' + getAlgorithmColorClass(_norm(cls.class_name)) + '"></span></div>';
        html += '<span class="class-pct">' + c + '%</span>';
        html += '</div>';
      });
      html += '</div>';
      html += '</div>';
    }

    html += '</div>';
    resultDiv.innerHTML = html;
  }

  function mostrarError(mensaje) {
    const msg = document.getElementById('msg');
    msg.textContent = mensaje;
    msg.className = 'msg error';
  }

  // Enter para clasificar
  document.getElementById('texto').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
      e.preventDefault();
      clasificar();
    }
  });
</script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/classify', methods=['POST'])
def api_classify():
    api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
    if not api_key:
        return jsonify({"error": "API key no configurada. Pega tu API key y clasifica."}), 400

    data = request.json
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({"error": "Texto vacío"}), 400

    try:
        response = requests.post(ml4k_url(api_key, "classify"), json={"data": text}, timeout=30)
        if not response.ok:
            return jsonify({"error": f"Error del modelo (código {response.status_code}). ¿Está entrenado?"}), response.status_code

        response_data = response.json()
        if not response_data:
            return jsonify({"error": "No se detectó ninguna clase"}), 404

        classifications = sorted(response_data, key=lambda x: x.get('confidence', 0), reverse=True)
        for cls in classifications:
            conf = round(float(cls.get('confidence', 0)), 1)
            cls['confidence'] = conf
            cls['algorithm_type'] = get_algorithm_type(cls.get('class_name'))
            cls['confidence_pct'] = f"{conf:g}%"
            cls['confidence_level'] = get_confidence_level(conf)

        return jsonify({
            "classifications": classifications,
            "top_result": classifications[0]
        })
    except requests.exceptions.Timeout:
        return jsonify({"error": "Timeout: el modelo tardó demasiado en responder"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/status', methods=['GET'])
def api_status():
    api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
    if not api_key:
        return jsonify({"status": 0, "msg": "Ingresa tu API key de ML for Kids", "type": "text"})
    try:
        resp = requests.get(ml4k_url(api_key, "status"), timeout=10)
        if resp.ok:
            return jsonify(resp.json())
        return jsonify({"status": 0, "msg": f"Error: {resp.status_code} - Modelo no encontrado o no entrenado", "type": "text"})
    except Exception as e:
        return jsonify({"status": 0, "msg": str(e), "type": "text"})


if __name__ == "__main__":
    print("Iniciando en http://127.0.0.1:5000")
    app.run(debug=False, port=5000, host="0.0.0.0")