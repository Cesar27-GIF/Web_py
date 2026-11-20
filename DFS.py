"""Aplicación Web Full-Stack (Python + HTML/SVG) · Búsqueda en Profundidad (DFS).

Caso de uso: Las Llaves Perdidas en la Casa.
- Backend en Python puro (sin instalar dependencias externas):
  * Construye el grafo bidireccional de la casa y gestiona puertas bloqueadas.
  * Ejecuta el algoritmo DFS generando todos los pasos físicos de ida y vuelta.
  * Calcula la distancia mínima real (BFS) para el diagnóstico comparativo.
  * Expone una API JSON en `POST /simular` y sirve la interfaz en `GET /`.
- Frontend interactivo en HTML5 / Tailwind / SVG:
  * Plano arquitectónico con texturas de piso, muros, ventanas y 14 muebles ilustrados.
  * Detective animado con linterna nocturna, sonido sintetizado y puertas bloqueables.

Ejecución:
    python app_dfs_llaves.py
    Abrir en el navegador: http://localhost:8000
"""

from collections import deque
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


# ---------- Datos arquitectónicos y grafo base de la casa ----------
LUGARES = {
    "Pasillo":     {"x": 388, "y": 125, "cuarto": "Vestíbulo", "icono": "🚪", "tipo": "pasillo"},
    "Sala":        {"x": 155, "y": 115, "cuarto": "Sala",      "icono": "🛋️", "tipo": "sala"},
    "Sofá":        {"x": 95,  "y": 255, "cuarto": "Sala",      "icono": "🛋️", "tipo": "sofa"},
    "Escritorio":  {"x": 210, "y": 255, "cuarto": "Sala",      "icono": "🖥️", "tipo": "escritorio"},
    "Cajón 1":     {"x": 160, "y": 425, "cuarto": "Sala",      "icono": "🗄️", "tipo": "cajon"},
    "Cajón 2":     {"x": 245, "y": 425, "cuarto": "Sala",      "icono": "🗄️", "tipo": "cajon"},
    "Cocina":      {"x": 630, "y": 125, "cuarto": "Cocina",    "icono": "🍳", "tipo": "cocina"},
    "Mesa Cocina": {"x": 565, "y": 310, "cuarto": "Cocina",    "icono": "🍽️", "tipo": "mesa"},
    "Alacena":     {"x": 690, "y": 310, "cuarto": "Cocina",    "icono": "🥫", "tipo": "alacena"},
    "Recámara":    {"x": 388, "y": 330, "cuarto": "Recámara",  "icono": "🛏️", "tipo": "recamara"},
    "Cama":        {"x": 330, "y": 455, "cuarto": "Recámara",  "icono": "🛌", "tipo": "cama"},
    "Clóset":      {"x": 445, "y": 425, "cuarto": "Recámara",  "icono": "🚪", "tipo": "closet"},
    "Abrigo":      {"x": 445, "y": 505, "cuarto": "Recámara",  "icono": "🧥", "tipo": "abrigo"},
    "En el Auto":  {"x": 870, "y": 280, "cuarto": "Cochera",   "icono": "🚗", "tipo": "auto"},
}

CONEXIONES_BASE = [
    ["Pasillo", "Sala"],
    ["Pasillo", "Cocina"],
    ["Pasillo", "Recámara"],
    ["Sala", "Escritorio"],
    ["Sala", "Sofá"],
    ["Escritorio", "Cajón 1"],
    ["Escritorio", "Cajón 2"],
    ["Cocina", "Mesa Cocina"],
    ["Cocina", "Alacena"],
    ["Recámara", "Cama"],
    ["Recámara", "Clóset"],
    ["Clóset", "Abrigo"],
]


def _clave_arista(a, b):
    """Genera una clave normalizada independiente del sentido."""
    return "::".join(sorted([a, b]))


def construir_grafo(bloqueos=None):
    """Construye el grafo bidireccional de la casa omitiendo puertas cerradas."""
    bloqueados = set(bloqueos or [])
    grafo = {lugar: [] for lugar in LUGARES}

    for a, b in CONEXIONES_BASE:
        if _clave_arista(a, b) in bloqueados:
            continue
        if b not in grafo[a]:
            grafo[a].append(b)
        if a not in grafo[b]:
            grafo[b].append(a)

    return grafo


def distancia_minima_bfs(grafo, inicio, objetivo):
    """Calcula la distancia mínima real (en saltos) usando BFS como referencia."""
    if inicio not in grafo or objetivo not in grafo:
        return None

    cola = deque([(inicio, 0)])
    visitados = {inicio}

    while cola:
        actual, dist = cola.popleft()
        if actual == objetivo:
            return dist
        for vecino in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, dist + 1))

    return None


def generar_recorrido_dfs(inicio, objetivo, bloqueos=None):
    """Ejecuta DFS en Python y construye la secuencia completa de pasos físicos (ida y vuelta)."""
    if inicio not in LUGARES:
        raise ValueError(f"El lugar inicial '{inicio}' no existe.")
    if objetivo not in LUGARES:
        raise ValueError(f"El destino '{objetivo}' no existe.")

    grafo = construir_grafo(bloqueos)
    pila = [(inicio, [inicio], 0)]
    visitados = {inicio}
    pasos = []
    aristas_ida = []
    aristas_vuelta = []
    retrocesos = 0
    camino_anterior = None

    while pila:
        nodo, camino, profundidad = pila.pop()

        # Reconstruir caminata física de regreso (backtracking) y avance
        if camino_anterior is not None:
            k = 0
            while (
                k < len(camino_anterior)
                and k < len(camino)
                and camino_anterior[k] == camino[k]
            ):
                k += 1

            # Pasos físicos de retroceso corredor por corredor
            for idx in range(len(camino_anterior) - 1, k - 1, -1):
                desde = camino_anterior[idx]
                hacia = camino_anterior[idx - 1]
                aristas_vuelta.append([desde, hacia])
                pasos.append({
                    "tipo": "retroceso",
                    "nodo": hacia,
                    "desde": desde,
                    "hacia": hacia,
                    "camino": camino_anterior[:idx],
                    "profundidad": idx - 1,
                    "retrocesos": retrocesos,
                    "visitados": sorted(visitados),
                    "aristasIda": [list(par) for par in aristas_ida],
                    "aristasVuelta": [list(par) for par in aristas_vuelta],
                    "encontrado": False,
                    "callejonSinSalida": False,
                    "titulo": f"↩️ Retrocedo hacia {hacia}",
                    "detalle": f"Regreso desde {desde} hasta {hacia} buscando una rama pendiente.",
                })

            # Registrar tramos de avance hacia la nueva rama
            for idx in range(k, len(camino)):
                aristas_ida.append([camino[idx - 1], camino[idx]])

        visitados.add(nodo)
        es_objetivo = nodo == objetivo
        nuevos = [v for v in grafo.get(nodo, []) if v not in visitados]

        for vecino in reversed(nuevos):
            visitados.add(vecino)
            pila.append((vecino, camino + [vecino], profundidad + 1))

        callejon_sin_salida = False
        if es_objetivo:
            tipo = "encontrado"
            titulo = f"🎉 ¡Llaves encontradas en {nodo}!"
            detalle = f"Ruta completa: {' → '.join(camino)} ({len(camino) - 1} saltos)."
        elif camino_anterior is None:
            tipo = "inicio"
            titulo = f"🕵️ Empiezo en {nodo}"
            detalle = (
                f"No están a la vista. Exploro en profundidad primero hacia {nuevos[0]}."
                if nuevos
                else f"{nodo} no tiene salidas conectadas."
            )
        elif nuevos:
            tipo = "avance"
            titulo = f"⬇️ Profundizo en {nodo}"
            detalle = f"No están aquí. Sigo bajando por esta rama hacia {nuevos[0]}."
        elif pila:
            tipo = "callejon"
            callejon_sin_salida = True
            retrocesos += 1
            siguiente = pila[-1][0]
            titulo = f"❌ {nodo} está vacío (callejón sin salida)"
            detalle = f"Llegué al fondo de esta rama. Volveré hacia {siguiente}."
        else:
            tipo = "agotado"
            callejon_sin_salida = True
            titulo = f"🚫 {nodo} vacío · Fin del recorrido"
            detalle = f"Revisé todos los lugares alcanzables desde {inicio} y las llaves no están ahí."

        pasos.append({
            "tipo": tipo,
            "nodo": nodo,
            "desde": camino[-2] if len(camino) > 1 else None,
            "hacia": nodo,
            "camino": list(camino),
            "profundidad": profundidad,
            "retrocesos": retrocesos,
            "visitados": sorted(visitados),
            "aristasIda": [list(par) for par in aristas_ida],
            "aristasVuelta": [list(par) for par in aristas_vuelta],
            "encontrado": es_objetivo,
            "callejonSinSalida": callejon_sin_salida,
            "titulo": titulo,
            "detalle": detalle,
        })

        camino_anterior = list(camino)
        if es_objetivo:
            break

    ultimo = pasos[-1]
    encontrado = bool(ultimo and ultimo["encontrado"])
    camino_ganador = ultimo["camino"] if encontrado else []
    saltos_optimos = distancia_minima_bfs(grafo, inicio, objetivo) if encontrado else None

    return {
        "pasos": pasos,
        "encontrado": encontrado,
        "caminoGanador": camino_ganador,
        "retrocesos": retrocesos,
        "saltosOptimos": saltos_optimos,
    }


# ---------- Frontend HTML + CSS + SVG + Cliente JS ----------
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Búsqueda en Profundidad (DFS) · Python + Web</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    body {
      font-family: "Inter", system-ui, -apple-system, sans-serif;
      background-color: #f8fafc;
      color: #1e293b;
    }

    @keyframes pulsoHalo {
      0%, 100% { transform: scale(1); opacity: 0.75; }
      50% { transform: scale(1.14); opacity: 0.28; }
    }
    .halo-activo {
      transform-box: fill-box;
      transform-origin: center;
      animation: pulsoHalo 1.5s ease-in-out infinite;
    }

    @keyframes flotarLlave {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-4px); }
    }
    .llave-flotante {
      transform-box: fill-box;
      transform-origin: center;
      animation: flotarLlave 1.8s ease-in-out infinite;
    }

    @keyframes sacudidaMueble {
      0%, 100% { transform: translateX(0); }
      20% { transform: translateX(-4px); }
      40% { transform: translateX(4px); }
      60% { transform: translateX(-3px); }
      80% { transform: translateX(3px); }
    }
    .mueble-vacio {
      transform-box: fill-box;
      transform-origin: center;
      animation: sacudidaMueble 0.45s ease-in-out;
    }

    @keyframes flujoPasillo {
      to { stroke-dashoffset: -24; }
    }
    .pasillo-animado {
      animation: flujoPasillo 1.1s linear infinite;
    }

    .detective-grupo,
    .linterna-grupo {
      transition: transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
    }

    .tira-scroll::-webkit-scrollbar { height: 6px; }
    .tira-scroll::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 999px; }
    .tira-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 999px; }
  </style>
</head>
<body class="min-h-screen pb-10">

  <!-- Encabezado superior -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3.5 flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 rounded-2xl bg-amber-100 border border-amber-300 flex items-center justify-center text-2xl shadow-xs">
          🔑
        </div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <h1 class="text-lg sm:text-xl font-extrabold text-slate-900 tracking-tight leading-tight">
              Búsqueda en Profundidad (DFS) · Las Llaves Perdidas
            </h1>
            <span class="px-2 py-0.5 rounded-full text-[11px] font-bold bg-indigo-100 text-indigo-800 border border-indigo-200">
              🐍 Motor Python Activo
            </span>
          </div>
          <p class="text-xs sm:text-sm text-slate-500">
            Haz clic en cualquier mueble para esconder las llaves o en un pasillo para cerrar la puerta con candado.
          </p>
        </div>
      </div>

      <!-- Interruptores visuales y de audio -->
      <div class="flex items-center gap-2 flex-wrap">
        <button id="btn-rayosx" type="button"
          class="px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold border border-amber-300 bg-amber-50 text-amber-800 hover:bg-amber-100 transition cursor-pointer">
          👁️ Rayos-X: ON
        </button>
        <button id="btn-noche" type="button"
          class="px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold border border-slate-300 bg-slate-100 text-slate-700 hover:bg-slate-200 transition cursor-pointer">
          ☀️ Modo Día
        </button>
        <button id="btn-sonido" type="button"
          class="px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold border border-indigo-200 bg-indigo-50 text-indigo-700 hover:bg-indigo-100 transition cursor-pointer">
          🔊 Sonido: ON
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 mt-5 space-y-4">

    <!-- Panel de configuración de escenario -->
    <section class="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
        <div class="md:col-span-3">
          <label for="sel-inicio" class="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
            🚪 Empezar búsqueda en
          </label>
          <select id="sel-inicio"
            class="w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-400">
          </select>
        </div>

        <div class="md:col-span-3">
          <label for="sel-objetivo" class="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
            🔑 Esconder llaves en
          </label>
          <select id="sel-objetivo"
            class="w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-amber-400">
          </select>
        </div>

        <!-- Escenarios rápidos -->
        <div class="md:col-span-6 flex flex-wrap items-center gap-2 md:justify-end">
          <button id="btn-esc-cocina" type="button"
            class="px-3 py-2 rounded-xl text-xs font-bold bg-indigo-600 text-white hover:bg-indigo-700 shadow-xs transition cursor-pointer">
            🍳 Cocina → Cajón 1
          </button>
          <button id="btn-esc-abrigo" type="button"
            class="px-3 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200 transition cursor-pointer">
            🧥 Pasillo → Abrigo
          </button>
          <button id="btn-esc-bloqueo" type="button"
            class="px-3 py-2 rounded-xl text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200 hover:bg-rose-100 transition cursor-pointer">
            🔒 Sala cerrada
          </button>
          <button id="btn-azar" type="button"
            class="px-3 py-2 rounded-xl text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 transition cursor-pointer">
            🎲 Al azar
          </button>
        </div>
      </div>
    </section>

    <!-- Barra de controles de reproducción y métricas -->
    <section class="bg-white rounded-2xl border border-slate-200 p-3.5 shadow-xs flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-1.5 flex-wrap">
        <button id="btn-ini" type="button" title="Ir al inicio"
          class="px-2.5 py-1.5 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 text-sm font-bold text-slate-700 cursor-pointer">
          ⏮
        </button>
        <button id="btn-ant" type="button" title="Paso anterior"
          class="px-2.5 py-1.5 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 text-sm font-bold text-slate-700 cursor-pointer">
          ◀
        </button>
        <button id="btn-play" type="button"
          class="px-4 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs sm:text-sm font-bold shadow-xs transition cursor-pointer">
          ⏸ Pausar
        </button>
        <button id="btn-sig" type="button" title="Paso siguiente"
          class="px-2.5 py-1.5 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 text-sm font-bold text-slate-700 cursor-pointer">
          ▶
        </button>

        <input id="slider-paso" type="range" min="0" max="0" value="0"
          class="w-28 sm:w-44 accent-indigo-600 mx-1.5 cursor-pointer" />

        <select id="sel-vel" title="Velocidad de animación"
          class="rounded-xl border border-slate-200 bg-slate-50 px-2.5 py-1.5 text-xs font-semibold text-slate-700">
          <option value="1300">0.75x Lento</option>
          <option value="850" selected>1x Normal</option>
          <option value="450">2x Rápido</option>
        </select>
      </div>

      <!-- Indicadores en tiempo real -->
      <div class="flex items-center gap-2 flex-wrap text-xs font-bold">
        <span id="stat-paso" class="px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
          Paso 1 / 1
        </span>
        <span id="stat-visitados" class="px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
          Revisados: 1 / 14
        </span>
        <span id="stat-retrocesos" class="px-2.5 py-1 rounded-full bg-rose-50 text-rose-700 border border-rose-200">
          Retrocesos: 0
        </span>
        <span id="stat-prof" class="px-2.5 py-1 rounded-full bg-amber-50 text-amber-800 border border-amber-200">
          Profundidad: 0
        </span>
      </div>
    </section>

    <!-- Banner narrativo del paso actual -->
    <section id="banner-accion"
      class="rounded-2xl border border-indigo-200 bg-indigo-50/90 px-4 py-3 flex items-center gap-3 transition-colors">
      <div id="banner-icono" class="text-2xl select-none">🕵️</div>
      <div class="min-w-0 flex-1">
        <div id="banner-titulo" class="text-xs sm:text-sm font-extrabold uppercase tracking-wide text-indigo-900">
          Iniciando búsqueda
        </div>
        <p id="banner-detalle" class="text-xs sm:text-sm text-indigo-800 truncate sm:whitespace-normal">
          Consultando algoritmo DFS en Python...
        </p>
      </div>
    </section>

    <!-- Plano Arquitectónico Interactivo de la Casa -->
    <section class="bg-white rounded-3xl border border-slate-200 p-3 sm:p-5 shadow-sm">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-3 px-1">
        <div class="flex items-center gap-4 flex-wrap text-xs font-semibold text-slate-600">
          <span class="flex items-center gap-1.5">
            <span class="inline-block w-4 h-1 bg-indigo-500 rounded"></span> ➡️ Camino de ida
          </span>
          <span class="flex items-center gap-1.5">
            <span class="inline-block w-4 h-0.5 border-t-2 border-dashed border-rose-500"></span> ↩️ Retroceso (vuelta)
          </span>
          <span class="flex items-center gap-1.5">
            <span class="inline-block w-4 h-1.5 bg-emerald-500 rounded"></span> 🎉 Ruta ganadora
          </span>
          <span class="flex items-center gap-1.5">
            🔒 Clic en pasillo = cerrar puerta
          </span>
        </div>
        <span id="stat-pct" class="text-xs font-bold text-slate-500">
          Casa explorada: 7%
        </span>
      </div>

      <div class="w-full overflow-hidden rounded-2xl border border-slate-200 bg-slate-100">
        <svg id="mapa-svg" viewBox="0 0 980 560" class="w-full h-auto block select-none"></svg>
      </div>

      <!-- Tira interactiva del recorrido físico de ida y vuelta -->
      <div class="mt-3.5">
        <div class="flex items-center justify-between mb-1.5 px-1">
          <span class="text-xs font-bold uppercase tracking-wider text-slate-500">
            👣 Recorrido físico paso a paso (clic para saltar)
          </span>
          <span class="text-[11px] text-slate-400">
            ➡️ Avance · ↩️ Vuelta
          </span>
        </div>
        <div id="tira-pasos" class="tira-scroll flex items-center gap-1.5 overflow-x-auto pb-1.5"></div>
      </div>
    </section>

    <!-- Panel de diagnóstico final -->
    <section id="panel-diagnostico" class="hidden rounded-2xl border p-4 sm:p-5 shadow-xs transition-all">
      <div class="flex items-start gap-3.5">
        <div id="diag-icono" class="text-3xl">🎉</div>
        <div class="flex-1 space-y-1.5">
          <h2 id="diag-titulo" class="text-base sm:text-lg font-extrabold"></h2>
          <p id="diag-texto" class="text-sm leading-relaxed"></p>
          <div id="diag-ruta" class="text-xs font-bold px-3 py-2 rounded-xl bg-white/70 border border-black/10 inline-block"></div>
          <p id="diag-metricas" class="text-xs opacity-85 pt-0.5"></p>
        </div>
      </div>
    </section>

  </main>

  <script>
    (() => {
      const SVG_NS = "http://www.w3.org/2000/svg";
      const $ = (id) => document.getElementById(id);

      // Datos inyectados directamente desde Python
      const LUGARES = __LUGARES_JSON__;
      const CONEXIONES_BASE = __CONEXIONES_JSON__;

      const estado = {
        inicio: "Cocina",
        objetivo: "Cajón 1",
        bloqueos: new Set(),
        pasos: [],
        indice: 0,
        reproduciendo: true,
        velocidad: 850,
        rayosX: true,
        modoNoche: false,
        sonido: true,
        timer: null,
        resultadoFinal: null
      };

      let audioCtx = null;

      function reproducirSonido(tipo) {
        if (!estado.sonido) return;
        try {
          if (!audioCtx) {
            const Ctx = window.AudioContext || window.webkitAudioContext;
            if (!Ctx) return;
            audioCtx = new Ctx();
          }
          if (audioCtx.state === "suspended") audioCtx.resume();

          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          const ahora = audioCtx.currentTime;

          osc.connect(gain);
          gain.connect(audioCtx.destination);

          if (tipo === "avance") {
            osc.type = "sine";
            osc.frequency.setValueAtTime(420, ahora);
            osc.frequency.exponentialRampToValueAtTime(580, ahora + 0.09);
            gain.gain.setValueAtTime(0.06, ahora);
            gain.gain.exponentialRampToValueAtTime(0.001, ahora + 0.1);
            osc.start(ahora);
            osc.stop(ahora + 0.11);
          } else if (tipo === "retroceso") {
            osc.type = "triangle";
            osc.frequency.setValueAtTime(320, ahora);
            osc.frequency.exponentialRampToValueAtTime(210, ahora + 0.12);
            gain.gain.setValueAtTime(0.06, ahora);
            gain.gain.exponentialRampToValueAtTime(0.001, ahora + 0.13);
            osc.start(ahora);
            osc.stop(ahora + 0.14);
          } else if (tipo === "encontrado") {
            osc.type = "triangle";
            osc.frequency.setValueAtTime(523.25, ahora);
            osc.frequency.setValueAtTime(659.25, ahora + 0.09);
            osc.frequency.setValueAtTime(783.99, ahora + 0.18);
            osc.frequency.setValueAtTime(1046.5, ahora + 0.27);
            gain.gain.setValueAtTime(0.09, ahora);
            gain.gain.exponentialRampToValueAtTime(0.001, ahora + 0.45);
            osc.start(ahora);
            osc.stop(ahora + 0.46);
          } else if (tipo === "bloqueo") {
            osc.type = "square";
            osc.frequency.setValueAtTime(180, ahora);
            gain.gain.setValueAtTime(0.04, ahora);
            gain.gain.exponentialRampToValueAtTime(0.001, ahora + 0.08);
            osc.start(ahora);
            osc.stop(ahora + 0.09);
          }
        } catch (_) {}
      }

      const claveArista = (a, b) => [a, b].sort().join("::");

      function crearElSVG(tag, attrs, texto) {
        const el = document.createElementNS(SVG_NS, tag);
        for (const k in attrs) {
          el.setAttribute(k, attrs[k]);
        }
        if (texto !== undefined) {
          el.textContent = texto;
        }
        return el;
      }

      function dibujarMuebleIlustrado(grupo, tipo, cx, cy, abierto, noche) {
        const madera = noche ? "#92400e" : "#d97706";
        const maderaOsc = noche ? "#78350f" : "#b45309";
        const tela = noche ? "#4338ca" : "#818cf8";
        const metal = noche ? "#64748b" : "#94a3b8";

        if (tipo === "pasillo") {
          grupo.appendChild(crearElSVG("rect", { x: cx - 32, y: cy - 11, width: 64, height: 27, rx: 5, fill: noche ? "#334155" : "#fed7aa", stroke: "#c2410c", "stroke-width": 1.4 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 28, y: cy - 7, width: 56, height: 19, rx: 3, fill: "none", stroke: "#ea580c", "stroke-width": 1, "stroke-dasharray": "3 2" }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 22, y: cy - 17, width: 44, height: 10, rx: 3, fill: madera, stroke: maderaOsc, "stroke-width": 1.4 }));
          grupo.appendChild(crearElSVG("circle", { cx, cy: cy - 12, r: 3.2, fill: "#fef08a", stroke: "#ca8a04", "stroke-width": 1 }));
        } else if (tipo === "sala") {
          grupo.appendChild(crearElSVG("rect", { x: cx - 35, y: cy - 16, width: 70, height: 32, rx: 10, fill: noche ? "#1e1b4b" : "#e0e7ff", stroke: "#6366f1", "stroke-width": 1.4 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 21, y: cy - 9, width: 42, height: 18, rx: 5, fill: madera, stroke: maderaOsc, "stroke-width": 1.5 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 14, y: cy - 5, width: 12, height: 9, rx: 1.5, fill: "#ffffff", stroke: "#94a3b8", "stroke-width": 1 }));
          grupo.appendChild(crearElSVG("circle", { cx: cx + 10, cy: cy, r: 5.5, fill: "#16a34a", stroke: "#14532d", "stroke-width": 1.1 }));
          grupo.appendChild(crearElSVG("circle", { cx: cx + 10, cy: cy, r: 2.3, fill: "#86efac" }));
        } else if (tipo === "recamara") {
          grupo.appendChild(crearElSVG("ellipse", { cx, cy: cy + 2, rx: 34, ry: 15, fill: noche ? "#31102f" : "#fce7f3", stroke: "#db2777", "stroke-width": 1.3 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 26, y: cy - 15, width: 52, height: 15, rx: 4, fill: madera, stroke: maderaOsc, "stroke-width": 1.5 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 16, y: cy - 18, width: 32, height: 5, rx: 2, fill: "#bae6fd", stroke: "#0284c7", "stroke-width": 1.2 }));
          grupo.appendChild(crearElSVG("circle", { cx, cy: cy + 8, r: 6.5, fill: "#f472b6", stroke: "#9d174d", "stroke-width": 1.3 }));
        } else if (tipo === "sofa") {
          grupo.appendChild(crearElSVG("rect", { x: cx - 34, y: cy - 14, width: 68, height: 28, rx: 7, fill: tela, stroke: "#312e81", "stroke-width": 1.5 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 34, y: cy - 14, width: 68, height: 8, rx: 4, fill: "#4f46e5", stroke: "#312e81", "stroke-width": 1.2 }));
          [-16, 0, 16].forEach((dx) => {
            grupo.appendChild(crearElSVG("rect", { x: cx + dx - 7, y: cy - 4, width: 14, height: 14, rx: 3, fill: noche ? "#6366f1" : "#a5b4fc", stroke: "#3730a3", "stroke-width": 1 }));
          });
          grupo.appendChild(crearElSVG("rect", { x: cx - 37, y: cy - 11, width: 7, height: 23, rx: 3, fill: "#4338ca", stroke: "#312e81", "stroke-width": 1.1 }));
          grupo.appendChild(crearElSVG("rect", { x: cx + 30, y: cy - 11, width: 7, height: 23, rx: 3, fill: "#4338ca", stroke: "#312e81", "stroke-width": 1.1 }));
        } else if (tipo === "escritorio") {
          grupo.appendChild(crearElSVG("rect", { x: cx - 32, y: cy - 13, width: 64, height: 24, rx: 4, fill: madera, stroke: maderaOsc, "stroke-width": 1.6 }));
          grupo.appendChild(crearElSVG("circle", { cx, cy: cy + 12, r: 7, fill: "#334155", stroke: "#0f172a", "stroke-width": 1.2 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 11, y: cy - 6, width: 22, height: 13, rx: 2, fill: "#e2e8f0", stroke: "#475569", "stroke-width": 1.2 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 9, y: cy - 9, width: 18, height: 4, rx: 1, fill: "#38bdf8", stroke: "#0284c7", "stroke-width": 1 }));
          grupo.appendChild(crearElSVG("circle", { cx: cx + 21, cy: cy - 5, r: 4.5, fill: "#fde047", stroke: "#ca8a04", "stroke-width": 1.1 }));
        } else if (tipo === "cajon") {
          const desp = abierto ? 6 : 0;
          grupo.appendChild(crearElSVG("rect", { x: cx - 22, y: cy - 14, width: 44, height: 22, rx: 4, fill: maderaOsc, stroke: "#451a03", "stroke-width": 1.5 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 20, y: cy - 8 + desp, width: 40, height: 14, rx: 3, fill: madera, stroke: "#451a03", "stroke-width": 1.4 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 7, y: cy - 2 + desp, width: 14, height: 3, rx: 1.5, fill: "#fef08a", stroke: "#78350f", "stroke-width": 0.9 }));
        } else if (tipo === "cocina") {
          grupo.appendChild(crearElSVG("rect", { x: cx - 34, y: cy - 14, width: 68, height: 26, rx: 4, fill: noche ? "#334155" : "#e2e8f0", stroke: "#475569", "stroke-width": 1.6 }));
          [[-21, -6], [-9, -6], [-21, 5], [-9, 5]].forEach(([qx, qy]) => {
            grupo.appendChild(crearElSVG("circle", { cx: cx + qx, cy: cy + qy, r: 4, fill: "#0f172a", stroke: "#f97316", "stroke-width": 1.2 }));
          });
          grupo.appendChild(crearElSVG("rect", { x: cx + 5, y: cy - 9, width: 22, height: 16, rx: 3, fill: "#bae6fd", stroke: "#0284c7", "stroke-width": 1.2 }));
          grupo.appendChild(crearElSVG("circle", { cx: cx + 16, cy: cy - 1, r: 2, fill: "#475569" }));
        } else if (tipo === "mesa") {
          [[-14, -15], [14, -15], [-14, 13], [14, 13]].forEach(([sx, sy]) => {
            grupo.appendChild(crearElSVG("rect", { x: cx + sx - 6, y: cy + sy - 3, width: 12, height: 6, rx: 2, fill: "#475569" }));
          });
          grupo.appendChild(crearElSVG("rect", { x: cx - 26, y: cy - 12, width: 52, height: 24, rx: 6, fill: madera, stroke: maderaOsc, "stroke-width": 1.6 }));
          [[-13, 0], [13, 0]].forEach(([px, py]) => {
            grupo.appendChild(crearElSVG("circle", { cx: cx + px, cy: cy + py, r: 4.5, fill: "#ffffff", stroke: "#94a3b8", "stroke-width": 1 }));
          });
        } else if (tipo === "alacena") {
          const ap = abierto ? 4 : 0;
          grupo.appendChild(crearElSVG("rect", { x: cx - 26, y: cy - 14, width: 52, height: 24, rx: 4, fill: noche ? "#1e293b" : "#fef3c7", stroke: maderaOsc, "stroke-width": 1.6 }));
          [-13, 0, 13].forEach((fx, idx) => {
            const cols = ["#ef4444", "#22c55e", "#f59e0b"];
            grupo.appendChild(crearElSVG("circle", { cx: cx + fx, cy: cy - 3, r: 4, fill: cols[idx], stroke: "#334155", "stroke-width": 0.9 }));
          });
          grupo.appendChild(crearElSVG("rect", { x: cx - 25, y: cy + 5 + ap, width: 24, height: 4.5, rx: 2, fill: madera, stroke: maderaOsc, "stroke-width": 1.1 }));
          grupo.appendChild(crearElSVG("rect", { x: cx + 1, y: cy + 5 + ap, width: 24, height: 4.5, rx: 2, fill: madera, stroke: maderaOsc, "stroke-width": 1.1 }));
        } else if (tipo === "cama") {
          grupo.appendChild(crearElSVG("rect", { x: cx - 28, y: cy - 17, width: 56, height: 32, rx: 5, fill: "#ffffff", stroke: "#475569", "stroke-width": 1.5 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 30, y: cy - 19, width: 60, height: 6, rx: 2.5, fill: maderaOsc, stroke: "#451a03", "stroke-width": 1.2 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 27, y: cy - 3, width: 54, height: 17, rx: 3, fill: noche ? "#3b82f6" : "#60a5fa", stroke: "#1d4ed8", "stroke-width": 1.1 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 22, y: cy - 11, width: 18, height: 7, rx: 2.5, fill: "#f1f5f9", stroke: "#94a3b8", "stroke-width": 1 }));
          grupo.appendChild(crearElSVG("rect", { x: cx + 4, y: cy - 11, width: 18, height: 7, rx: 2.5, fill: "#f1f5f9", stroke: "#94a3b8", "stroke-width": 1 }));
        } else if (tipo === "closet") {
          grupo.appendChild(crearElSVG("rect", { x: cx - 28, y: cy - 14, width: 56, height: 24, rx: 4, fill: madera, stroke: maderaOsc, "stroke-width": 1.6 }));
          grupo.appendChild(crearElSVG("line", { x1: cx, y1: cy - 14, x2: cx, y2: cy + 10, stroke: "#451a03", "stroke-width": 1.5 }));
          grupo.appendChild(crearElSVG("circle", { cx: cx - 4, cy: cy - 2, r: 2, fill: "#fef08a" }));
          grupo.appendChild(crearElSVG("circle", { cx: cx + 4, cy: cy - 2, r: 2, fill: "#fef08a" }));
        } else if (tipo === "abrigo") {
          grupo.appendChild(crearElSVG("path", {
            d: `M ${cx - 10} ${cy - 13} L ${cx + 10} ${cy - 13} L ${cx + 22} ${cy - 2} L ${cx + 16} ${cy + 4} L ${cx + 11} ${cy - 2} L ${cx + 11} ${cy + 11} L ${cx - 11} ${cy + 11} L ${cx - 11} ${cy - 2} L ${cx - 16} ${cy + 4} L ${cx - 22} ${cy - 2} Z`,
            fill: "#0d9488", stroke: "#115e59", "stroke-width": 1.5, "stroke-linejoin": "round"
          }));
          grupo.appendChild(crearElSVG("line", { x1: cx, y1: cy - 13, x2: cx, y2: cy + 11, stroke: "#134e4a", "stroke-width": 1.2 }));
        } else if (tipo === "auto") {
          [[-22, -11], [16, -11], [-22, 8], [16, 8]].forEach(([wx, wy]) => {
            grupo.appendChild(crearElSVG("rect", { x: cx + wx, y: cy + wy, width: 8, height: 4, rx: 1.5, fill: "#0f172a" }));
          });
          grupo.appendChild(crearElSVG("rect", { x: cx - 28, y: cy - 10, width: 56, height: 21, rx: 7, fill: "#ef4444", stroke: "#991b1b", "stroke-width": 1.6 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 14, y: cy - 7, width: 28, height: 15, rx: 4, fill: "#bae6fd", stroke: "#0369a1", "stroke-width": 1.2 }));
          grupo.appendChild(crearElSVG("rect", { x: cx - 7, y: cy - 6, width: 14, height: 13, rx: 2, fill: "#dc2626" }));
          grupo.appendChild(crearElSVG("circle", { cx: cx + 26, cy: cy - 6, r: 2, fill: "#fef08a" }));
          grupo.appendChild(crearElSVG("circle", { cx: cx + 26, cy: cy + 6, r: 2, fill: "#fef08a" }));
        } else {
          grupo.appendChild(crearElSVG("ellipse", { cx, cy, rx: 34, ry: 19, fill: noche ? "#334155" : "#e2e8f0", stroke: metal, "stroke-width": 1.3 }));
        }
      }

      function renderizarMapa() {
        const svg = $("mapa-svg");
        const pasoActual = estado.pasos[estado.indice];
        const noche = estado.modoNoche;
        const setVisitados = new Set(pasoActual ? pasoActual.visitados : []);

        svg.innerHTML = "";
        const defs = crearElSVG("defs", {});

        const patMadera = crearElSVG("pattern", { id: "pat-madera", width: 28, height: 14, patternUnits: "userSpaceOnUse" });
        patMadera.appendChild(crearElSVG("rect", { width: 28, height: 14, fill: noche ? "#1e1b18" : "#fef3c7" }));
        patMadera.appendChild(crearElSVG("path", { d: "M 0 7 H 28 M 14 0 V 7 M 28 7 V 14", stroke: noche ? "#292524" : "#fde68a", "stroke-width": 1 }));
        defs.appendChild(patMadera);

        const patLoseta = crearElSVG("pattern", { id: "pat-loseta", width: 24, height: 24, patternUnits: "userSpaceOnUse" });
        patLoseta.appendChild(crearElSVG("rect", { width: 24, height: 24, fill: noche ? "#1e293b" : "#f1f5f9" }));
        patLoseta.appendChild(crearElSVG("path", { d: "M 24 0 H 0 V 24", fill: "none", stroke: noche ? "#334155" : "#e2e8f0", "stroke-width": 1 }));
        defs.appendChild(patLoseta);

        [["fl-ida", "#4f46e5"], ["fl-vuelta", "#e11d48"], ["fl-ganador", "#059669"]].forEach(([id, color]) => {
          const marker = crearElSVG("marker", {
            id, viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 6.5, markerHeight: 6.5, orient: "auto-start-reverse"
          });
          marker.appendChild(crearElSVG("path", { d: "M 0 1.5 L 9 5 L 0 8.5 z", fill: color }));
          defs.appendChild(marker);
        });

        const gradLinterna = crearElSVG("radialGradient", { id: "grad-linterna", cx: "50%", cy: "50%", r: "50%" });
        gradLinterna.appendChild(crearElSVG("stop", { offset: "0%", "stop-color": "#fef08a", "stop-opacity": "0.42" }));
        gradLinterna.appendChild(crearElSVG("stop", { offset: "55%", "stop-color": "#fde047", "stop-opacity": "0.14" }));
        gradLinterna.appendChild(crearElSVG("stop", { offset: "100%", "stop-color": "#fde047", "stop-opacity": "0" }));
        defs.appendChild(gradLinterna);

        svg.appendChild(defs);

        // Exterior
        svg.appendChild(crearElSVG("rect", { x: 0, y: 0, width: 980, height: 560, fill: noche ? "#090d16" : "#e2f0d9" }));
        svg.appendChild(crearElSVG("rect", { x: 356, y: 0, width: 64, height: 32, fill: noche ? "#1e293b" : "#cbd5e1" }));
        svg.appendChild(crearElSVG("rect", { x: 760, y: 245, width: 28, height: 70, fill: noche ? "#1e293b" : "#cbd5e1" }));

        // Habitaciones
        svg.appendChild(crearElSVG("rect", { x: 30, y: 30, width: 245, height: 500, fill: "url(#pat-madera)" }));
        svg.appendChild(crearElSVG("text", { x: 46, y: 52, "font-size": 11, "font-weight": "800", fill: noche ? "#fbbf24" : "#92400e", opacity: 0.75 }, "SALA DE ESTAR"));

        svg.appendChild(crearElSVG("rect", { x: 275, y: 30, width: 225, height: 240, fill: "url(#pat-loseta)" }));
        svg.appendChild(crearElSVG("text", { x: 290, y: 52, "font-size": 11, "font-weight": "800", fill: noche ? "#94a3b8" : "#475569", opacity: 0.8 }, "VESTÍBULO"));

        svg.appendChild(crearElSVG("rect", { x: 275, y: 270, width: 225, height: 260, fill: "url(#pat-madera)" }));
        svg.appendChild(crearElSVG("text", { x: 290, y: 292, "font-size": 11, "font-weight": "800", fill: noche ? "#fbbf24" : "#92400e", opacity: 0.75 }, "RECÁMARA PRINCIPAL"));

        svg.appendChild(crearElSVG("rect", { x: 500, y: 30, width: 260, height: 500, fill: "url(#pat-loseta)" }));
        svg.appendChild(crearElSVG("text", { x: 516, y: 52, "font-size": 11, "font-weight": "800", fill: noche ? "#94a3b8" : "#475569", opacity: 0.8 }, "COCINA"));

        svg.appendChild(crearElSVG("rect", {
          x: 785, y: 170, width: 170, height: 220, rx: 14,
          fill: noche ? "#111827" : "#e2e8f0", stroke: noche ? "#475569" : "#64748b", "stroke-width": 4
        }));
        svg.appendChild(crearElSVG("text", { x: 870, y: 194, "text-anchor": "middle", "font-size": 10.5, "font-weight": "800", fill: noche ? "#94a3b8" : "#475569" }, "COCHERA EXTERIOR"));
        svg.appendChild(crearElSVG("text", { x: 870, y: 208, "text-anchor": "middle", "font-size": 9.5, "font-weight": "600", fill: "#ef4444" }, "(Sin acceso interior)"));

        // Muros y puertas
        const colorMuro = noche ? "#475569" : "#334155";
        svg.appendChild(crearElSVG("rect", { x: 30, y: 30, width: 730, height: 500, rx: 10, fill: "none", stroke: colorMuro, "stroke-width": 7 }));

        svg.appendChild(crearElSVG("line", { x1: 275, y1: 30, x2: 275, y2: 92, stroke: colorMuro, "stroke-width": 5 }));
        svg.appendChild(crearElSVG("line", { x1: 275, y1: 148, x2: 275, y2: 530, stroke: colorMuro, "stroke-width": 5 }));
        svg.appendChild(crearElSVG("line", { x1: 500, y1: 30, x2: 500, y2: 97, stroke: colorMuro, "stroke-width": 5 }));
        svg.appendChild(crearElSVG("line", { x1: 500, y1: 153, x2: 500, y2: 530, stroke: colorMuro, "stroke-width": 5 }));
        svg.appendChild(crearElSVG("line", { x1: 275, y1: 270, x2: 360, y2: 270, stroke: colorMuro, "stroke-width": 5 }));
        svg.appendChild(crearElSVG("line", { x1: 416, y1: 270, x2: 500, y2: 270, stroke: colorMuro, "stroke-width": 5 }));

        [
          { x: 110, y: 27, w: 68, h: 6 },
          { x: 590, y: 27, w: 68, h: 6 },
          { x: 110, y: 527, w: 68, h: 6 },
          { x: 590, y: 527, w: 68, h: 6 },
          { x: 27, y: 220, w: 6, h: 74 },
          { x: 757, y: 220, w: 6, h: 74 }
        ].forEach((v) => {
          svg.appendChild(crearElSVG("rect", { x: v.x, y: v.y, width: v.w, height: v.h, rx: 2, fill: "#38bdf8", stroke: "#0284c7", "stroke-width": 1 }));
        });
        svg.appendChild(crearElSVG("rect", { x: 364, y: 26, width: 48, height: 8, rx: 2, fill: "#b45309" }));

        // Conexiones de ida y vuelta
        const setIda = new Set((pasoActual ? pasoActual.aristasIda : []).map(([a, b]) => `${a}->${b}`));
        const setVuelta = new Set((pasoActual ? pasoActual.aristasVuelta : []).map(([a, b]) => `${a}->${b}`));
        const setGanador = new Set();
        if (pasoActual && pasoActual.encontrado) {
          for (let i = 0; i < pasoActual.camino.length - 1; i++) {
            setGanador.add(`${pasoActual.camino[i]}->${pasoActual.camino[i + 1]}`);
          }
        }

        CONEXIONES_BASE.forEach(([a, b]) => {
          const pA = LUGARES[a];
          const pB = LUGARES[b];
          const key = claveArista(a, b);
          const bloqueada = estado.bloqueos.has(key);

          const dx = pB.x - pA.x;
          const dy = pB.y - pA.y;
          const dist = Math.hypot(dx, dy) || 1;
          const ux = dx / dist;
          const uy = dy / dist;
          const nx = -uy;
          const ny = ux;

          const x1 = pA.x + ux * 28;
          const y1 = pA.y + uy * 28;
          const x2 = pB.x - ux * 28;
          const y2 = pB.y - uy * 28;

          const gConexion = crearElSVG("g", { class: "cursor-pointer" });
          gConexion.addEventListener("click", (ev) => {
            ev.stopPropagation();
            if (estado.bloqueos.has(key)) estado.bloqueos.delete(key);
            else estado.bloqueos.add(key);
            reproducirSonido("bloqueo");
            recalcularSimulacion();
          });

          gConexion.appendChild(crearElSVG("line", { x1, y1, x2, y2, stroke: "transparent", "stroke-width": 20 }));
          gConexion.appendChild(crearElSVG("line", {
            x1, y1, x2, y2,
            stroke: bloqueada ? "#fda4af" : (noche ? "#475569" : "#cbd5e1"),
            "stroke-width": bloqueada ? 3 : 3.5,
            "stroke-dasharray": bloqueada ? "6 5" : "none",
            "stroke-linecap": "round"
          }));

          if (!bloqueada) {
            const idaAB = setIda.has(`${a}->${b}`);
            const idaBA = setIda.has(`${b}->${a}`);
            const ganAB = setGanador.has(`${a}->${b}`);
            const ganBA = setGanador.has(`${b}->${a}`);

            if (idaAB || idaBA || ganAB || ganBA) {
              const esGan = ganAB || ganBA;
              const dirForward = ganAB || (!ganBA && idaAB);
              const sx = (dirForward ? x1 : x2) + nx * 4.5;
              const sy = (dirForward ? y1 : y2) + ny * 4.5;
              const ex = (dirForward ? x2 : x1) + nx * 4.5;
              const ey = (dirForward ? y2 : y1) + ny * 4.5;

              gConexion.appendChild(crearElSVG("line", {
                x1: sx, y1: sy, x2: ex, y2: ey,
                stroke: esGan ? "#059669" : "#4f46e5",
                "stroke-width": esGan ? 4.2 : 3,
                "stroke-linecap": "round",
                "marker-end": `url(#${esGan ? "fl-ganador" : "fl-ida"})`
              }));
            }

            const vueltaAB = setVuelta.has(`${a}->${b}`);
            const vueltaBA = setVuelta.has(`${b}->${a}`);
            if (vueltaAB || vueltaBA) {
              const vx1 = (vueltaAB ? x1 : x2) - nx * 5.5;
              const vy1 = (vueltaAB ? y1 : y2) - ny * 5.5;
              const vx2 = (vueltaAB ? x2 : x1) - nx * 5.5;
              const vy2 = (vueltaAB ? y2 : y1) - ny * 5.5;

              gConexion.appendChild(crearElSVG("line", {
                x1: vx1, y1: vy1, x2: vx2, y2: vy2,
                stroke: "#e11d48",
                "stroke-width": 2.6,
                "stroke-dasharray": "5 4",
                "stroke-linecap": "round",
                class: "pasillo-animado",
                "marker-end": "url(#fl-vuelta)"
              }));
            }
          } else {
            const mx = (x1 + x2) / 2;
            const my = (y1 + y2) / 2;
            gConexion.appendChild(crearElSVG("circle", { cx: mx, cy: my, r: 12, fill: "#ffe4e6", stroke: "#e11d48", "stroke-width": 1.8 }));
            gConexion.appendChild(crearElSVG("text", { x: mx, y: my + 4, "text-anchor": "middle", "font-size": 12 }, "🔒"));
          }

          svg.appendChild(gConexion);
        });

        // Muebles y lugares
        Object.entries(LUGARES).forEach(([nombre, info]) => {
          const esActual = pasoActual && pasoActual.nodo === nombre;
          const estaVisitado = setVisitados.has(nombre);
          const esInicio = nombre === estado.inicio;
          const tieneLlaves = nombre === estado.objetivo;
          const halladaAqui = Boolean(pasoActual && pasoActual.encontrado && esActual);
          const vacioAqui = Boolean(pasoActual && pasoActual.callejonSinSalida && esActual);

          const gNodo = crearElSVG("g", { class: "cursor-pointer" });
          gNodo.addEventListener("click", () => {
            estado.objetivo = nombre;
            $("sel-objetivo").value = nombre;
            recalcularSimulacion();
          });

          if (esActual) {
            gNodo.appendChild(crearElSVG("circle", {
              cx: info.x, cy: info.y, r: 34,
              fill: halladaAqui ? "#10b981" : (vacioAqui ? "#f43f5e" : "#f59e0b"),
              class: "halo-activo"
            }));
          }

          const gMueble = crearElSVG("g", { class: vacioAqui ? "mueble-vacio" : "" });
          dibujarMuebleIlustrado(gMueble, info.tipo, info.x, info.y, estaVisitado || esActual, noche);
          gNodo.appendChild(gMueble);

          let pillFill = noche ? "#1e293b" : "#ffffff";
          let pillStroke = noche ? "#475569" : "#cbd5e1";
          let pillText = noche ? "#f8fafc" : "#1e293b";

          if (halladaAqui) {
            pillFill = "#059669"; pillStroke = "#064e3b"; pillText = "#ffffff";
          } else if (vacioAqui) {
            pillFill = "#ffe4e6"; pillStroke = "#e11d48"; pillText = "#9f1239";
          } else if (esActual) {
            pillFill = "#fef3c7"; pillStroke = "#d97706"; pillText = "#92400e";
          } else if (estaVisitado) {
            pillFill = noche ? "#1e3a8a" : "#dbeafe"; pillStroke = "#3b82f6"; pillText = noche ? "#dbeafe" : "#1e40af";
          } else if (esInicio) {
            pillFill = "#e0e7ff"; pillStroke = "#6366f1"; pillText = "#3730a3";
          }

          const anchoEtiqueta = Math.max(92, nombre.length * 7.4 + 34);
          gNodo.appendChild(crearElSVG("rect", {
            x: info.x - anchoEtiqueta / 2, y: info.y + 13, width: anchoEtiqueta, height: 21, rx: 8,
            fill: pillFill, stroke: pillStroke, "stroke-width": esActual || halladaAqui ? 2 : 1.3
          }));

          gNodo.appendChild(crearElSVG("text", {
            x: info.x, y: info.y + 27, "text-anchor": "middle", "font-size": 10.5, "font-weight": "800", fill: pillText
          }, halladaAqui ? `🎉 ${nombre}` : `${info.icono} ${nombre}`));

          if (esInicio && !halladaAqui) {
            gNodo.appendChild(crearElSVG("rect", { x: info.x - 24, y: info.y - 31, width: 48, height: 14, rx: 5, fill: "#4f46e5" }));
            gNodo.appendChild(crearElSVG("text", { x: info.x, y: info.y - 21, "text-anchor": "middle", "font-size": 8.5, "font-weight": "800", fill: "#ffffff" }, "INICIO"));
          }

          if (tieneLlaves && (estado.rayosX || halladaAqui)) {
            const gLlave = crearElSVG("g", { class: "llave-flotante" });
            gLlave.appendChild(crearElSVG("circle", { cx: info.x + 26, cy: info.y - 18, r: 12, fill: "#fef08a", stroke: "#ca8a04", "stroke-width": 1.6 }));
            gLlave.appendChild(crearElSVG("text", { x: info.x + 26, y: info.y - 13.5, "text-anchor": "middle", "font-size": 13 }, "🔑"));
            gNodo.appendChild(gLlave);
          }

          svg.appendChild(gNodo);
        });

        // Detective animado
        const detective = pasoActual ? LUGARES[pasoActual.nodo] : LUGARES[estado.inicio];
        if (detective) {
          if (noche) {
            const gLinterna = crearElSVG("g", { class: "linterna-grupo", transform: `translate(${detective.x}, ${detective.y})` });
            gLinterna.appendChild(crearElSVG("circle", { cx: 0, cy: 0, r: 135, fill: "url(#grad-linterna)", "pointer-events": "none" }));
            svg.appendChild(gLinterna);
          }

          const gDet = crearElSVG("g", { class: "detective-grupo", transform: `translate(${detective.x - 28}, ${detective.y - 16})` });
          gDet.appendChild(crearElSVG("circle", { cx: 0, cy: 0, r: 14, fill: "#ffffff", stroke: "#0f172a", "stroke-width": 2 }));
          gDet.appendChild(crearElSVG("text", { x: 0, y: 5, "text-anchor": "middle", "font-size": 16 }, pasoActual && pasoActual.encontrado ? "🥳" : "🕵️"));
          svg.appendChild(gDet);
        }
      }

      function renderizarTiraPasos() {
        const cont = $("tira-pasos");
        cont.innerHTML = "";

        estado.pasos.forEach((p, idx) => {
          const activo = idx === estado.indice;
          const btn = document.createElement("button");
          btn.type = "button";

          let clases = "shrink-0 px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer ";
          if (activo) {
            clases += "bg-slate-900 text-white border-slate-900 shadow-xs scale-105";
          } else if (p.tipo === "encontrado") {
            clases += "bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100";
          } else if (p.tipo === "retroceso" || p.tipo === "callejon") {
            clases += "bg-rose-50 text-rose-700 border-rose-200 hover:bg-rose-100";
          } else {
            clases += "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100";
          }

          btn.className = clases;
          const flecha = p.tipo === "retroceso" ? "↩️" : (p.tipo === "encontrado" ? "🎉" : "➡️");
          btn.textContent = `${idx + 1}. ${flecha} ${p.nodo}`;
          btn.addEventListener("click", () => {
            pausarAuto();
            irAPaso(idx, false);
          });

          cont.appendChild(btn);
        });

        const chipActivo = cont.children[estado.indice];
        if (chipActivo) {
          chipActivo.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
        }
      }

      function irAPaso(nuevoIndice, conSonido = true) {
        if (estado.pasos.length === 0) return;
        estado.indice = Math.max(0, Math.min(estado.pasos.length - 1, nuevoIndice));

        const paso = estado.pasos[estado.indice];
        const totalPasos = estado.pasos.length;
        const totalLugares = Object.keys(LUGARES).length;

        if (conSonido) {
          if (paso.tipo === "encontrado") reproducirSonido("encontrado");
          else if (paso.tipo === "retroceso" || paso.tipo === "callejon") reproducirSonido("retroceso");
          else if (paso.tipo === "avance") reproducirSonido("avance");
        }

        $("slider-paso").max = Math.max(0, totalPasos - 1);
        $("slider-paso").value = estado.indice;
        $("stat-paso").textContent = `Paso ${estado.indice + 1} / ${totalPasos}`;
        $("stat-visitados").textContent = `Revisados: ${paso.visitados.length} / ${totalLugares}`;
        $("stat-retrocesos").textContent = `Retrocesos: ${paso.retrocesos}`;
        $("stat-prof").textContent = `Profundidad: ${paso.profundidad}`;
        $("stat-pct").textContent = `Casa explorada: ${Math.round((paso.visitados.length / totalLugares) * 100)}%`;

        const banner = $("banner-accion");
        const bIcono = $("banner-icono");
        const bTitulo = $("banner-titulo");
        const bDetalle = $("banner-detalle");

        bTitulo.textContent = paso.titulo;
        bDetalle.textContent = paso.detalle;

        if (paso.tipo === "encontrado") {
          banner.className = "rounded-2xl border border-emerald-300 bg-emerald-50 px-4 py-3 flex items-center gap-3";
          bTitulo.className = "text-xs sm:text-sm font-extrabold uppercase tracking-wide text-emerald-900";
          bDetalle.className = "text-xs sm:text-sm text-emerald-800";
          bIcono.textContent = "🎉";
        } else if (paso.tipo === "retroceso" || paso.tipo === "callejon") {
          banner.className = "rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 flex items-center gap-3";
          bTitulo.className = "text-xs sm:text-sm font-extrabold uppercase tracking-wide text-rose-900";
          bDetalle.className = "text-xs sm:text-sm text-rose-800";
          bIcono.textContent = paso.tipo === "retroceso" ? "↩️" : "🛑";
        } else {
          banner.className = "rounded-2xl border border-indigo-200 bg-indigo-50 px-4 py-3 flex items-center gap-3";
          bTitulo.className = "text-xs sm:text-sm font-extrabold uppercase tracking-wide text-indigo-900";
          bDetalle.className = "text-xs sm:text-sm text-indigo-800";
          bIcono.textContent = "🕵️";
        }

        const panelDiag = $("panel-diagnostico");
        if (estado.indice === totalPasos - 1 && estado.resultadoFinal) {
          const res = estado.resultadoFinal;
          panelDiag.classList.remove("hidden");

          if (res.encontrado) {
            const saltosDFS = res.caminoGanador.length - 1;
            const huboRodeo = res.saltosOptimos !== null && saltosDFS > res.saltosOptimos;

            panelDiag.className = "rounded-2xl border border-emerald-300 bg-emerald-50/90 text-emerald-950 p-4 sm:p-5 shadow-xs";
            $("diag-icono").textContent = "🎉";
            $("diag-titulo").textContent = `¡Llaves encontradas en ${estado.objetivo}!`;
            $("diag-texto").textContent = huboRodeo
              ? `Python DFS llegó en ${saltosDFS} saltos (el camino más corto posible era de ${res.saltosOptimos} saltos, pero el algoritmo profundizó primero por otras ramas).`
              : `Python DFS encontró las llaves en ${saltosDFS} salto(s), coincidiendo con el camino más directo.`;
            $("diag-ruta").classList.remove("hidden");
            $("diag-ruta").textContent = `Ruta ganadora: ${res.caminoGanador.join(" → ")}`;
            $("diag-metricas").textContent = `Movimientos físicos totales: ${totalPasos} · Retrocesos en callejones sin salida: ${res.retrocesos}`;
          } else {
            panelDiag.className = "rounded-2xl border border-rose-300 bg-rose-50/90 text-rose-950 p-4 sm:p-5 shadow-xs";
            $("diag-icono").textContent = "🔒";
            $("diag-titulo").textContent = `No se pudo llegar a ${estado.objetivo}`;
            $("diag-texto").textContent = `"${estado.objetivo}" quedó aislado de "${estado.inicio}" (está en la cochera exterior o detrás de una puerta cerrada con candado).`;
            $("diag-ruta").classList.add("hidden");
            $("diag-metricas").textContent = `Lugares revisados antes de agotar toda la zona accesible: ${paso.visitados.length} · Retrocesos: ${res.retrocesos}`;
          }
        } else {
          panelDiag.classList.add("hidden");
        }

        renderizarMapa();
        renderizarTiraPasos();
        actualizarBotonPlay();
      }

      function actualizarBotonPlay() {
        const btn = $("btn-play");
        if (estado.reproduciendo) btn.textContent = "⏸ Pausar";
        else if (estado.indice >= estado.pasos.length - 1) btn.textContent = "↻ Repetir";
        else btn.textContent = "▶ Reproducir";
      }

      function pausarAuto() {
        estado.reproduciendo = false;
        if (estado.timer) {
          clearInterval(estado.timer);
          estado.timer = null;
        }
        actualizarBotonPlay();
      }

      function iniciarAuto() {
        if (estado.timer) clearInterval(estado.timer);
        estado.reproduciendo = true;
        actualizarBotonPlay();

        estado.timer = setInterval(() => {
          if (!estado.reproduciendo) return;
          if (estado.indice < estado.pasos.length - 1) {
            irAPaso(estado.indice + 1, true);
          } else {
            pausarAuto();
          }
        }, estado.velocidad);
      }

      // Consulta al servidor Python (/simular) para ejecutar DFS y recibir los pasos
      async function recalcularSimulacion() {
        try {
          const resp = await fetch("/simular", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              inicio: estado.inicio,
              objetivo: estado.objetivo,
              bloqueos: Array.from(estado.bloqueos)
            })
          });
          const data = await resp.json();
          if (data.error) {
            $("banner-titulo").textContent = "Error en simulación";
            $("banner-detalle").textContent = data.error;
            return;
          }
          estado.pasos = data.pasos;
          estado.resultadoFinal = data;
          irAPaso(0, false);
          iniciarAuto();
        } catch (err) {
          $("banner-titulo").textContent = "Sin conexión con el servidor Python";
          $("banner-detalle").textContent = "Verifica que python app_dfs_llaves.py siga ejecutándose en consola.";
        }
      }

      function inicializarSelectores() {
        const nombres = Object.keys(LUGARES);
        const selIni = $("sel-inicio");
        const selObj = $("sel-objetivo");
        selIni.innerHTML = "";
        selObj.innerHTML = "";

        nombres.forEach((nombre) => {
          const info = LUGARES[nombre];
          const opt1 = document.createElement("option");
          opt1.value = nombre;
          opt1.textContent = `${info.icono} ${nombre} (${info.cuarto})`;
          selIni.appendChild(opt1);

          const opt2 = document.createElement("option");
          opt2.value = nombre;
          opt2.textContent = `${info.icono} ${nombre} (${info.cuarto})`;
          selObj.appendChild(opt2);
        });

        selIni.value = estado.inicio;
        selObj.value = estado.objetivo;
      }

      $("sel-inicio").addEventListener("change", (e) => { estado.inicio = e.target.value; recalcularSimulacion(); });
      $("sel-objetivo").addEventListener("change", (e) => { estado.objetivo = e.target.value; recalcularSimulacion(); });

      $("btn-esc-cocina").addEventListener("click", () => {
        estado.bloqueos.clear();
        estado.inicio = "Cocina";
        estado.objetivo = "Cajón 1";
        $("sel-inicio").value = estado.inicio;
        $("sel-objetivo").value = estado.objetivo;
        recalcularSimulacion();
      });

      $("btn-esc-abrigo").addEventListener("click", () => {
        estado.bloqueos.clear();
        estado.inicio = "Pasillo";
        estado.objetivo = "Abrigo";
        $("sel-inicio").value = estado.inicio;
        $("sel-objetivo").value = estado.objetivo;
        recalcularSimulacion();
      });

      $("btn-esc-bloqueo").addEventListener("click", () => {
        estado.bloqueos.clear();
        estado.bloqueos.add(claveArista("Pasillo", "Sala"));
        estado.inicio = "Cocina";
        estado.objetivo = "Cajón 1";
        $("sel-inicio").value = estado.inicio;
        $("sel-objetivo").value = estado.objetivo;
        recalcularSimulacion();
      });

      $("btn-azar").addEventListener("click", () => {
        const nombres = Object.keys(LUGARES).filter((n) => n !== estado.inicio && n !== "En el Auto");
        const elegido = nombres[Math.floor(Math.random() * nombres.length)];
        estado.objetivo = elegido;
        estado.rayosX = false;
        $("sel-objetivo").value = elegido;
        $("btn-rayosx").textContent = "🙈 Rayos-X: OFF";
        $("btn-rayosx").className = "px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold border border-slate-300 bg-slate-100 text-slate-700 hover:bg-slate-200 transition cursor-pointer";
        recalcularSimulacion();
      });

      $("btn-rayosx").addEventListener("click", () => {
        estado.rayosX = !estado.rayosX;
        const btn = $("btn-rayosx");
        btn.textContent = estado.rayosX ? "👁️ Rayos-X: ON" : "🙈 Rayos-X: OFF";
        btn.className = estado.rayosX
          ? "px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold border border-amber-300 bg-amber-50 text-amber-800 hover:bg-amber-100 transition cursor-pointer"
          : "px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold border border-slate-300 bg-slate-100 text-slate-700 hover:bg-slate-200 transition cursor-pointer";
        renderizarMapa();
      });

      $("btn-noche").addEventListener("click", () => {
        estado.modoNoche = !estado.modoNoche;
        const btn = $("btn-noche");
        btn.textContent = estado.modoNoche ? "🔦 Modo Noche" : "☀️ Modo Día";
        btn.className = estado.modoNoche
          ? "px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold border border-amber-400 bg-slate-900 text-amber-300 hover:bg-slate-800 transition cursor-pointer"
          : "px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold border border-slate-300 bg-slate-100 text-slate-700 hover:bg-slate-200 transition cursor-pointer";
        renderizarMapa();
      });

      $("btn-sonido").addEventListener("click", () => {
        estado.sonido = !estado.sonido;
        $("btn-sonido").textContent = estado.sonido ? "🔊 Sonido: ON" : "🔇 Sonido: OFF";
      });

      $("btn-ini").addEventListener("click", () => { pausarAuto(); irAPaso(0, false); });
      $("btn-ant").addEventListener("click", () => { pausarAuto(); irAPaso(estado.indice - 1, false); });
      $("btn-sig").addEventListener("click", () => { pausarAuto(); irAPaso(estado.indice + 1, true); });

      $("btn-play").addEventListener("click", () => {
        if (estado.reproduciendo) {
          pausarAuto();
        } else {
          if (estado.indice >= estado.pasos.length - 1) irAPaso(0, false);
          iniciarAuto();
        }
      });

      $("slider-paso").addEventListener("input", (e) => { pausarAuto(); irAPaso(Number(e.target.value), false); });
      $("sel-vel").addEventListener("change", (e) => {
        estado.velocidad = Number(e.target.value);
        if (estado.reproduciendo) iniciarAuto();
      });

      inicializarSelectores();
      recalcularSimulacion();
    })();
  </script>
</body>
</html>
"""


def renderizar_html():
    """Inyecta el diccionario de lugares y conexiones como JSON dentro de la plantilla HTML."""
    return (
        HTML_TEMPLATE
        .replace("__LUGARES_JSON__", json.dumps(LUGARES, ensure_ascii=False))
        .replace("__CONEXIONES_JSON__", json.dumps(CONEXIONES_BASE, ensure_ascii=False))
    )


# ---------- Servidor HTTP integrado ----------
class DFSWebHandler(BaseHTTPRequestHandler):
    """Manejador HTTP que sirve la página web en GET / y ejecuta DFS en POST /simular."""

    def _responder(self, codigo, content_type, contenido_bytes):
        self.send_response(codigo)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(contenido_bytes)))
        self.end_headers()
        self.wfile.write(contenido_bytes)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html_bytes = renderizar_html().encode("utf-8")
            self._responder(200, "text/html; charset=utf-8", html_bytes)
        else:
            self._responder(404, "text/plain; charset=utf-8", b"Ruta no encontrada")

    def do_POST(self):
        if self.path != "/simular":
            self._responder(404, "application/json; charset=utf-8", b'{"error": "Ruta no encontrada"}')
            return

        try:
            longitud = int(self.headers.get("Content-Length", 0))
            cuerpo = json.loads(self.rfile.read(longitud).decode("utf-8"))
            inicio = cuerpo.get("inicio", "Cocina")
            objetivo = cuerpo.get("objetivo", "Cajón 1")
            bloqueos = cuerpo.get("bloqueos", [])

            resultado = generar_recorrido_dfs(inicio, objetivo, bloqueos=bloqueos)
            payload = json.dumps(resultado, ensure_ascii=False).encode("utf-8")
            self._responder(200, "application/json; charset=utf-8", payload)
        except Exception as err:
            error_payload = json.dumps({"error": str(err)}, ensure_ascii=False).encode("utf-8")
            self._responder(400, "application/json; charset=utf-8", error_payload)

    def log_message(self, format, *args):
        """Silencia el registro de cada petición estática para mantener limpia la consola."""
        pass


if __name__ == "__main__":
    PUERTO = 8000
    servidor = HTTPServer(("localhost", PUERTO), DFSWebHandler)
    print(f"Servidor Python + Web activo en: http://localhost:{PUERTO}")
    print("Presiona Ctrl + C para detener el servidor.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        servidor.server_close()