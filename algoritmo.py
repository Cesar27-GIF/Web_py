"""
Módulo: Algoritmos de Búsqueda en Inteligencia Artificial
Contiene la investigación completa sobre algoritmos de búsqueda:
  (a) Definición y criterios de evaluación
  (b) Elementos que intervienen en un algoritmo de búsqueda
  (c) Ejemplo paso a paso identificando cada elemento (BFS en un laberinto)
  (d) Clasificación por múltiples criterios (ciega, heurística, local, adversarial, CSP...)
  (e) Datos de la infografía: taxonomía visual, tabla comparativa, historia y aplicaciones
"""


# =========================================================================
# (a) ¿QUÉ ES UN ALGORITMO DE BÚSQUEDA?
# =========================================================================
DEFINICION = {
    "titulo": "¿Qué es un Algoritmo de Búsqueda?",
    "definicion": (
        "Un algoritmo de búsqueda es un procedimiento sistemático, finito y bien definido "
        "que explora de manera organizada un conjunto de posibilidades (llamado espacio de estados) "
        "para localizar un elemento, una configuración o un camino que resuelva un problema, "
        "decidiendo en cada paso cuál alternativa expandir según una estrategia fija."
    ),
    "definicion_ia": (
        "En Inteligencia Artificial, la búsqueda es el método universal de resolución de problemas: "
        "el problema se modela como un grafo donde los nodos son estados del mundo y las aristas son "
        "acciones que transforman un estado en otro. Resolver el problema equivale a encontrar un "
        "camino que va del estado inicial al estado objetivo."
    ),
    "nota_datos": (
        "En estructuras de datos clásicas, 'buscar' significa localizar un elemento dentro de una "
        "colección ya almacenada (búsqueda lineal, binaria o por hash). En IA el concepto se generaliza: "
        "no buscamos dentro de un dato existente, sino entre todas las acciones posibles — el camino "
        "solución no existe de antemano, se construye paso a paso."
    ),
    "por_que_importa": (
        "La búsqueda es el corazón de la IA clásica: planificar la ruta de un robot, elegir la jugada "
        "ganadora en un juego, resolver un puzzle o asignar horarios son, en esencia, problemas de "
        "búsqueda. La diferencia entre un agente brillante y uno inútil está en qué estrategia elige "
        "y cuánto del espacio logra evitar explorar."
    )
}

# Criterios con los que se evalúa cualquier algoritmo de búsqueda
CRITERIOS_EVALUACION = [
    {
        "nombre": "Completitud",
        "corto": "Completitud",
        "icono": "fa-circle-check",
        "desc": "¿Si existe una solución, el algoritmo garantiza encontrarla?"
    },
    {
        "nombre": "Optimalidad",
        "corto": "Optimalidad",
        "icono": "fa-medal",
        "desc": "¿La solución hallada es la de menor costo entre todas las posibles?"
    },
    {
        "nombre": "Complejidad temporal",
        "corto": "Tiempo",
        "icono": "fa-clock",
        "desc": "¿Cuánto tarda, medido en nodos expandidos, según el tamaño del problema (b, d, m)?"
    },
    {
        "nombre": "Complejidad espacial",
        "corto": "Memoria",
        "icono": "fa-memory",
        "desc": "¿Cuánta memoria necesita para guardar la frontera y los estados visitados?"
    }
]


# =========================================================================
# (b) ELEMENTOS QUE INTERVIENEN EN UN ALGORITMO DE BÚSQUEDA
# =========================================================================
ELEMENTOS = [
    {
        "id": 1,
        "nombre": "Espacio de estados",
        "icono": "fa-sitemap",
        "def": "El universo de todas las configuraciones posibles del problema, conectadas por acciones. Formalmente es un grafo dirigido: nodos = estados, aristas = transiciones.",
        "ejemplo": "Las 8 salas del laberinto y sus pasadizos."
    },
    {
        "id": 2,
        "nombre": "Estado inicial",
        "icono": "fa-play",
        "def": "La configuración donde comienza la búsqueda. Es el primer nodo que entra en la frontera.",
        "ejemplo": "El robot en la sala A."
    },
    {
        "id": 3,
        "nombre": "Estado objetivo y prueba de meta",
        "icono": "fa-flag-checkered",
        "def": "La configuración que satisface el problema, junto con la función que permite reconocerla al generarla (¿es este estado la solución?).",
        "ejemplo": "La sala H (salida): es_meta(estado) == (estado == 'H')."
    },
    {
        "id": 4,
        "nombre": "Acciones (operadores)",
        "icono": "fa-gears",
        "def": "Los movimientos válidos que transforman un estado en otro. Definen la arista y el costo de avanzar en el grafo.",
        "ejemplo": "Cruzar una puerta hacia una sala adyacente."
    },
    {
        "id": 5,
        "nombre": "Camino y solución",
        "icono": "fa-route",
        "def": "Secuencia ordenada de acciones que lleva del estado inicial al objetivo. La solución puede ser el camino completo o solo el estado final, según el problema.",
        "ejemplo": "A → B → D → F → H."
    },
    {
        "id": 6,
        "nombre": "Función de coste g(n)",
        "icono": "fa-coins",
        "def": "Número que acumula el costo del camino recorrido hasta el estado n (tiempo, distancia, dinero, energía...). El algoritmo intenta minimizar el costo total.",
        "ejemplo": "1 punto por puerta cruzada: el camino solución cuesta g = 4."
    },
    {
        "id": 7,
        "nombre": "Función heurística h(n)",
        "icono": "fa-wand-magic-sparkles",
        "def": "Estimación —no garantizada pero razonable— del costo restante desde n hasta la meta. Solo la usan los algoritmos informados. Si nunca sobreestima, se dice admisible.",
        "ejemplo": "No se usa en BFS (ciega); en A* sería la distancia en línea recta a la salida."
    },
    {
        "id": 8,
        "nombre": "Frontera (fringe)",
        "icono": "fa-layer-group",
        "def": "Conjunto de nodos ya generados pero aún no expandidos. Es la 'lista de pendientes' del algoritmo; el ciclo de búsqueda saca un nodo de aquí y genera sus hijos.",
        "ejemplo": "La cola FIFO de salas descubiertas que faltan por explorar."
    },
    {
        "id": 9,
        "nombre": "Estrategia de búsqueda",
        "icono": "fa-shuffle",
        "def": "La regla que decide qué nodo de la frontera se expande primero (el más antiguo, el más barato, el más prometedor...). La estrategia es lo que distingue a BFS de DFS, de A* o de Greedy.",
        "ejemplo": "FIFO = 'el más antiguo primero' = exploración por anchura (BFS)."
    }
]


# =========================================================================
# (c) EJEMPLO: BFS ENCONTRANDO LA SALIDA DE UN LABERINTO
# =========================================================================
EJEMPLO = {
    "titulo": "Ejemplo: un robot encuentra la salida con BFS",
    "problema": (
        "Un robot está en la sala A de un laberinto de 8 salas y debe llegar a la puerta de salida, "
        "en la sala H. Solo puede moverse por las puertas que conectan salas adyacentes y cada puerta "
        "cuesta exactamente 1 punto de energía. Se usa búsqueda en anchura (BFS): explorar el "
        "laberinto por niveles, como una mancha de agua que se extiende."
    ),
    "mapa": (
        "      A ----- B ----- D ----- F\n"
        "      |                       |\n"
        "      C ----- E ----- G ----- H\n"
        "\n"
        "  INICIO: A (robot)      META: H (salida)\n"
        "  Cada linea = una puerta que cuesta 1"
    ),
    "pasos": [
        {"paso": "0", "expande": "—", "frontera": "[A]", "nota": "Se parte del estado inicial: la frontera contiene solo A."},
        {"paso": "1", "expande": "A", "frontera": "[B, C]", "nota": "Se expande A y se generan sus vecinos B y C. Ninguno es la meta."},
        {"paso": "2", "expande": "B", "frontera": "[C, D]", "nota": "FIFO: sale el más antiguo (B) y se agrega su hijo nuevo D."},
        {"paso": "3", "expande": "C", "frontera": "[D, E]", "nota": "Sale C y se agrega E. El nivel 1 (B, C) quedó explorado completo."},
        {"paso": "4", "expande": "D", "frontera": "[E, F]", "nota": "Nivel 2: D agrega a F (A y B ya están visitados)."},
        {"paso": "5", "expande": "E", "frontera": "[F, G]", "nota": "E agrega a G. La salida todavía no aparece."},
        {"paso": "6", "expande": "F", "frontera": "[G, H]", "nota": "¡Al expandir F se genera H! H pasa la prueba de meta: el algoritmo termina y reconstruye el camino A → B → D → F → H."}
    ],
    "identificacion": [
        {"elemento": "Espacio de estados", "en_ejemplo": "Las 8 salas (A–H) conectadas por puertas."},
        {"elemento": "Estado inicial", "en_ejemplo": "El robot en la sala A."},
        {"elemento": "Estado objetivo / prueba de meta", "en_ejemplo": "La sala H; la prueba es es_meta(estado)."},
        {"elemento": "Acciones (operadores)", "en_ejemplo": "Cruzar una puerta hacia una sala adyacente."},
        {"elemento": "Frontera", "en_ejemplo": "La cola FIFO de salas descubiertas pendientes."},
        {"elemento": "Estrategia de búsqueda", "en_ejemplo": "FIFO (el más antiguo primero) = anchura."},
        {"elemento": "Camino y solución", "en_ejemplo": "La secuencia A → B → D → F → H."},
        {"elemento": "Función de coste g(n)", "en_ejemplo": "1 punto por puerta: g = 4."},
        {"elemento": "Función heurística h(n)", "en_ejemplo": "No se usa: BFS es una búsqueda ciega."},
        {"elemento": "Criterios de evaluación", "en_ejemplo": "Completo y óptimo (costos iguales); tiempo y memoria O(b^d)."}
    ],
    "codigo": (
        "from collections import deque\n"
        "\n"
        "# ESPACIO DE ESTADOS: cada sala y sus pasadizos (grafo del problema)\n"
        "LABERINTO = {\n"
        "    'A': ['B', 'C'],   # desde A se puede cruzar a B o a C\n"
        "    'B': ['A', 'D'],\n"
        "    'C': ['A', 'E'],\n"
        "    'D': ['B', 'F'],\n"
        "    'E': ['C', 'G'],\n"
        "    'F': ['D', 'H'],\n"
        "    'G': ['E', 'H'],\n"
        "    'H': ['F', 'G'],   # ESTADO OBJETIVO: la salida\n"
        "}\n"
        "\n"
        "ESTADO_INICIAL = 'A'                     # el robot inicia en la sala A\n"
        "def es_meta(estado): return estado == 'H' # PRUEBA DE META: es la salida\n"
        "\n"
        "def bfs(inicio):\n"
        "    frontera = deque([[inicio]])   # FRONTERA: caminos pendientes de expandir\n"
        "    visitados = {inicio}          # salas ya generadas (evita ciclos)\n"
        "\n"
        "    while frontera:                        # mientras queden nodos por expandir\n"
        "        camino = frontera.popleft()        # ESTRATEGIA: FIFO -> anchura (BFS)\n"
        "        estado = camino[-1]                # estado actual = ultima sala del camino\n"
        "\n"
        "        if es_meta(estado):                # ¿cumple la prueba de meta?\n"
        "            return camino                  # SOLUCION: A -> B -> D -> F -> H\n"
        "\n"
        "        for vecino in LABERINTO[estado]:        # ACCIONES: cruzar cada puerta\n"
        "            if vecino not in visitados:         # solo salas nuevas\n"
        "                visitados.add(vecino)\n"
        "                # FUNCION DE COSTE g(n): cada puerta suma 1 (len-1)\n"
        "                frontera.append(camino + [vecino])\n"
        "    return None                     # espacio agotado: no hay solucion\n"
        "\n"
        "print(bfs(ESTADO_INICIAL))   # ['A', 'B', 'D', 'F', 'H']  ->  4 pasos, costo 4"
    ),
    "resultado": (
        "BFS devuelve el camino A → B → D → F → H con costo 4. Como BFS explora por niveles y todas "
        "las puertas cuestan lo mismo, ese camino es garantizadamente el más corto posible "
        "(completo y óptimo). DFS, en cambio, podría haberse ido por una rama profunda sin salida "
        "y devolver un camino mucho más largo."
    ),
    "moral": (
        "Moraleja: si las puertas costaran distinto (pasadizos de longitudes diferentes), BFS ya no "
        "garantizaría el mínimo costo: habría que usar Costo Uniforme (UCS/Dijkstra) o, mejor aún, "
        "A* con h(n) = distancia en línea recta a la salida. Ahí entra la clasificación siguiente."
    )
}


# =========================================================================
# (d) + (e) CLASIFICACIÓN DE ALGORITMOS DE BÚSQUEDA
# (taxonomía multi-criterio usada también por la infografía)
# =========================================================================
INTRO_CLASIFICACION = (
    "No existe UNA sola clasificación: un mismo algoritmo pertenece a varias categorías a la vez "
    "(A* es informada, de camino, exponencial en memoria y óptima si su heurística es admisible). "
    "Por eso se clasifica según criterios independientes:"
)

CLASIFICACION_BUSQUEDA = [
    {
        "id": "dominio",
        "numero": "1",
        "criterio": "Según la información del dominio",
        "icono": "fa-compass",
        "intro": "¿El algoritmo sabe algo más allá de la definición del problema?",
        "ramas": [
            {
                "nombre": "Búsqueda no informada (ciega)",
                "alias": "CIEGA / BLIND",
                "color": "#0284c7",
                "icono": "fa-map",
                "def": "No usa estimaciones: explora a ciegas basándose solo en las reglas del problema, sin pista de si se acerca o se aleja de la meta.",
                "algoritmos": ["BFS (anchura)", "DFS (profundidad)", "UCS (costo uniforme)", "DLS (profundidad limitada)", "IDS (profundidad iterativa)"]
            },
            {
                "nombre": "Búsqueda informada (heurística)",
                "alias": "HEURÍSTICA / INFORMED",
                "color": "#7c3aed",
                "icono": "fa-wand-magic-sparkles",
                "def": "Utiliza una función heurística h(n) que estima cuánto falta para la meta y prioriza expandir los caminos más prometedores.",
                "algoritmos": ["Greedy Best-First", "A*", "IDA*", "SMA*", "Beam Search"]
            }
        ]
    },
    {
        "id": "objetivo",
        "numero": "2",
        "criterio": "Según el objetivo de la búsqueda",
        "icono": "fa-bullseye",
        "intro": "¿Qué tipo de problema resuelve?",
        "ramas": [
            {
                "nombre": "Búsqueda de camino (pathfinding)",
                "alias": "RUTAS",
                "color": "#0284c7",
                "icono": "fa-route",
                "def": "Encuentra la ruta de un punto a otro en un grafo o mapa: importa el camino completo, no solo el destino.",
                "algoritmos": ["BFS", "DFS", "UCS", "A*", "IDA*"]
            },
            {
                "nombre": "Búsqueda local (optimización)",
                "alias": "LOCAL",
                "color": "#d97706",
                "icono": "fa-mountain",
                "def": "Mejora un estado moviéndose entre vecinos para maximizar o minimizar una función. No guarda el camino: solo importa el estado final. Ideal cuando el espacio es gigantesco.",
                "algoritmos": ["Hill Climbing", "Recocido Simulado", "Búsqueda Tabú", "Algoritmos Genéticos"]
            },
            {
                "nombre": "Búsqueda con adversario (juegos)",
                "alias": "ADVERSARIAL",
                "color": "#e11d48",
                "icono": "fa-chess-knight",
                "def": "Decide jugadas suponiendo un oponente que también juega de manera óptima: minimiza mi pérdida y maximiza mi ganancia.",
                "algoritmos": ["Minimax", "Poda Alfa-Beta", "MCTS (Monte Carlo)"]
            },
            {
                "nombre": "Búsqueda con restricciones (CSP)",
                "alias": "RESTRICCIONES",
                "color": "#059669",
                "icono": "fa-puzzle-piece",
                "def": "Busca combinaciones válidas de variables que cumplan un conjunto de reglas sin violar ninguna restricción.",
                "algoritmos": ["Backtracking", "Forward Checking", "AC-3"]
            }
        ]
    },
    {
        "id": "memoria",
        "numero": "3",
        "criterio": "Según el uso de memoria",
        "icono": "fa-memory",
        "intro": "¿Cuánta memoria necesita para recordar lo explorado?",
        "ramas": [
            {
                "nombre": "Memoria exponencial",
                "alias": "O(b^d)",
                "color": "#e11d48",
                "icono": "fa-database",
                "def": "Guarda todos los nodos generados en la frontera: completa y óptima, pero se queda sin memoria rápido.",
                "algoritmos": ["BFS", "UCS", "A*", "Greedy"]
            },
            {
                "nombre": "Memoria lineal",
                "alias": "O(b·d)",
                "color": "#0284c7",
                "icono": "fa-bars-staggered",
                "def": "Guarda solo el camino actual y sus hermanos: memoria proporcional a la profundidad.",
                "algoritmos": ["DFS", "DLS", "IDS", "IDA*"]
            },
            {
                "nombre": "Memoria acotada",
                "alias": "O(1) / configurable",
                "color": "#059669",
                "icono": "fa-feather",
                "def": "Memoria casi nula o limitada por diseño: sacrifican garantías a cambio de caber en cualquier máquina.",
                "algoritmos": ["SMA*", "Beam Search", "Hill Climbing"]
            }
        ]
    },
    {
        "id": "optimalidad",
        "numero": "4",
        "criterio": "Según la garantía de optimalidad",
        "icono": "fa-scale-balanced",
        "intro": "¿Garantizan la mejor solución o solo una solución rápida?",
        "ramas": [
            {
                "nombre": "Óptimos",
                "alias": "GARANTIZADO",
                "color": "#16a34a",
                "icono": "fa-medal",
                "def": "Garantizan siempre la mejor solución (menor costo), bajo sus condiciones de uso.",
                "algoritmos": ["BFS (costos iguales)", "UCS (costos iguales)", "A* (h admisible)", "IDA*", "Minimax + Alfa-Beta"]
            },
            {
                "nombre": "No óptimos",
                "alias": "SIN GARANTÍA",
                "color": "#ea580c",
                "icono": "fa-triangle-exclamation",
                "def": "Respuestas rápidas y baratas, pero no aseguran el menor costo: pueden quedarse en máximos locales.",
                "algoritmos": ["DFS", "DLS", "Greedy", "Hill Climbing", "Beam Search"]
            }
        ]
    }
]

# ¿Qué es cada algoritmo? Fichas de definición (inciso d)
FICHAS_ALGORITMOS = [
    {
        "corto": "BFS",
        "largo": "Búsqueda en Anchura (Breadth-First)",
        "familia": "Ciega",
        "color": "#0284c7",
        "que_es": "Explora el grafo por niveles, como una mancha de agua: primero los vecinos del inicio, luego los vecinos de los vecinos. Usa una cola FIFO y garantiza el camino con menos pasos cuando todos cuestan lo mismo."
    },
    {
        "corto": "DFS",
        "largo": "Búsqueda en Profundidad (Depth-First)",
        "familia": "Ciega",
        "color": "#0284c7",
        "que_es": "Se hunde por una sola rama hasta no poder avanzar y entonces retrocede. Usa una pila LIFO: gasta memoria mínima, pero puede meterse en ramas infinitas y devolver caminos enormes."
    },
    {
        "corto": "UCS",
        "largo": "Costo Uniforme (Dijkstra)",
        "familia": "Ciega",
        "color": "#0284c7",
        "que_es": "Expande siempre el camino más barato acumulado hasta ahora, g(n), sin importar cuántos pasos lleve. Es el Dijkstra de la IA: óptimo cuando las acciones cuestan distinto."
    },
    {
        "corto": "DLS",
        "largo": "Profundidad Limitada",
        "familia": "Ciega",
        "color": "#0284c7",
        "que_es": "Un DFS con tope: no puede bajar más allá de una profundidad máxima. Se salva de los caminos infinitos, pero si la meta está más abajo del límite, jamás la encuentra."
    },
    {
        "corto": "IDS",
        "largo": "Profundidad Iterativa",
        "familia": "Ciega",
        "color": "#0284c7",
        "que_es": "Repite DLS con límites crecientes (0, 1, 2...) hasta dar con la meta. Parece desperdiciar trabajo, pero combina lo mejor de BFS y DFS: óptimo y con memoria lineal."
    },
    {
        "corto": "Greedy",
        "largo": "Greedy Best-First (Búsqueda Ávida)",
        "familia": "Heurística",
        "color": "#7c3aed",
        "que_es": "Expande siempre el nodo que parece más cerca de la meta según h(n), ignorando lo que ya costó llegar hasta ahí. Muy rápido, pero se deja engañar y no garantiza el mejor camino."
    },
    {
        "corto": "A*",
        "largo": "A-Estrella",
        "familia": "Heurística",
        "color": "#7c3aed",
        "que_es": "El estándar de la búsqueda con heurística: expande el nodo con menor f(n) = g(n) + h(n), costo ya caminado más estimación restante. Con una h admisible devuelve siempre el camino más barato."
    },
    {
        "corto": "IDA*",
        "largo": "A* Iterativo en Profundidad",
        "familia": "Heurística",
        "color": "#7c3aed",
        "que_es": "A* sin lista de espera: hace búsquedas en profundidad con un presupuesto de costo cada vez mayor. Memoria lineal como DFS y óptimo como A*."
    },
    {
        "corto": "SMA*",
        "largo": "A* con Memoria Simplificada",
        "familia": "Heurística",
        "color": "#7c3aed",
        "que_es": "A* con presupuesto de memoria: cuando la frontera se llena, olvida el peor nodo y lo reaprende si vuelve a hacer falta. Óptimo si la solución cabe en la memoria disponible."
    },
    {
        "corto": "Beam",
        "largo": "Búsqueda en Haz (Beam Search)",
        "familia": "Heurística",
        "color": "#7c3aed",
        "que_es": "BFS por niveles que solo conserva los k nodos más prometedores de cada nivel (el 'haz' de luz). Barato y veloz, pero puede descartar el camino correcto."
    },
    {
        "corto": "Hill Climbing",
        "largo": "Ascenso de Colinas",
        "familia": "Local",
        "color": "#d97706",
        "que_es": "Búsqueda local: del estado actual solo se mueve al vecino que mejora la función objetivo, y se detiene cuando ningún vecino es mejor. Simple y veloz, pero se atasca en máximos locales."
    },
    {
        "corto": "Recocido Simulado",
        "largo": "Simulated Annealing",
        "familia": "Local",
        "color": "#d97706",
        "que_es": "Hill Climbing que a veces acepta empeorar, con una probabilidad que baja con el tiempo (se 'enfría'), imitando el temple del metal. Así logra escapar de los máximos locales."
    },
    {
        "corto": "Búsqueda Tabú",
        "largo": "Tabu Search",
        "familia": "Local",
        "color": "#d97706",
        "que_es": "Búsqueda local con memoria: lleva una lista tabú de movimientos recientes prohibidos, evitando dar vueltas en círculo y obligándose a explorar zonas nuevas del espacio."
    },
    {
        "corto": "Genéticos",
        "largo": "Algoritmos Genéticos",
        "familia": "Local",
        "color": "#d97706",
        "que_es": "Mantiene una población de soluciones candidatas que se cruzan y mutan; las más aptas sobreviven y se reproducen. Evolución simulada, ideal para espacios gigantescos."
    },
    {
        "corto": "Minimax",
        "largo": "Minimización del peor caso",
        "familia": "Adversarial",
        "color": "#e11d48",
        "que_es": "Para juegos de dos jugadores: yo maximizo mi ganancia y asumo que el rival minimiza la mía. Recorre el árbol de jugadas y elige la rama con el mejor peor-caso posible."
    },
    {
        "corto": "Poda Alfa-Beta",
        "largo": "Alpha-Beta Pruning",
        "familia": "Adversarial",
        "color": "#e11d48",
        "que_es": "Minimax inteligente: descarta las ramas que ya no pueden cambiar la decisión final. Devuelve la misma jugada explorando muchísimo menos: hasta el doble de profundidad útil."
    },
    {
        "corto": "MCTS",
        "largo": "Monte Carlo Tree Search",
        "familia": "Adversarial",
        "color": "#e11d48",
        "que_es": "Simula miles de finalizaciones aleatorias desde cada jugada candidata y elige las que más victorias producen. No necesita evaluar el árbol completo; es la base de AlphaGo."
    },
    {
        "corto": "Backtracking",
        "largo": "Vuelta Atrás",
        "familia": "CSP",
        "color": "#059669",
        "que_es": "Asigna valores a las variables una por una y retrocede en cuanto una regla se rompe. El método clásico de satisfacción de restricciones: sudokus, horarios, colorear mapas."
    },
    {
        "corto": "Forward Checking",
        "largo": "Comprobación Adelantada",
        "familia": "CSP",
        "color": "#059669",
        "que_es": "Acompaña al backtracking: al asignar una variable, borra al instante los valores imposibles de sus vecinas, detectando los conflictos mucho antes de expandir."
    },
    {
        "corto": "AC-3",
        "largo": "Consistencia de Arcos",
        "familia": "CSP",
        "color": "#059669",
        "que_es": "Algoritmo de propagación de restricciones: revisa pares de variables y elimina los valores sin soporte en la otra, repitiendo hasta que todo el grafo queda consistente."
    }
]

# Guía rápida de selección (¿cuál usar?)
GUIA_SELECCION = [
    {
        "pregunta": "¿No tienes heurística y todos los pasos cuestan lo mismo?",
        "recomendacion": "BFS o IDS",
        "porque": "IDS combina lo mejor de ambos: óptimo y con memoria lineal O(b·d)."
    },
    {
        "pregunta": "¿Sin heurística pero los pasos cuestan distinto?",
        "recomendacion": "UCS (Dijkstra)",
        "porque": "Expande siempre el camino con menor costo acumulado g(n)."
    },
    {
        "pregunta": "¿Tienes una heurística admisible (que nunca sobreestima)?",
        "recomendacion": "A* (o IDA* / SMA* si falta memoria)",
        "porque": "f(n) = g(n) + h(n): óptimo y expande muchísimos menos nodos."
    },
    {
        "pregunta": "¿Hay un adversario que juega en tu contra?",
        "recomendacion": "Minimax + poda Alfa-Beta (o MCTS)",
        "porque": "Supone al rival jugando óptimo y poda las ramas inútiles."
    },
    {
        "pregunta": "¿Solo importa el estado final y no el camino?",
        "recomendacion": "Hill Climbing, Recocido Simulado o Genéticos",
        "porque": "Búsqueda local: memoria casi nula, ideal para espacios gigantes."
    },
    {
        "pregunta": "¿Debes asignar valores cumpliendo reglas (CSP)?",
        "recomendacion": "Backtracking + Forward Checking",
        "porque": "Propaga restricciones y detecta conflictos antes de expandir."
    }
]

# Tabla comparativa de complejidades (datos de Russell & Norvig, AIMA)
TABLA_COMPARATIVA = [
    {"algoritmo": "BFS", "familia": "Ciega", "color": "#0284c7", "tiempo": "O(b^d)", "espacio": "O(b^d)", "optimo": "Sí (costos iguales)"},
    {"algoritmo": "DFS", "familia": "Ciega", "color": "#0284c7", "tiempo": "O(b^m)", "espacio": "O(b·m)", "optimo": "No"},
    {"algoritmo": "UCS", "familia": "Ciega", "color": "#0284c7", "tiempo": "O(b^(C*/ε))", "espacio": "Exponencial", "optimo": "Sí"},
    {"algoritmo": "IDS", "familia": "Ciega", "color": "#0284c7", "tiempo": "O(b^d)", "espacio": "O(b·d)", "optimo": "Sí (costos iguales)"},
    {"algoritmo": "Greedy", "familia": "Heurística", "color": "#7c3aed", "tiempo": "O(b^m)", "espacio": "O(b^m)", "optimo": "No"},
    {"algoritmo": "A*", "familia": "Heurística", "color": "#7c3aed", "tiempo": "O(b^d)", "espacio": "O(b^d)", "optimo": "Sí (h admisible)"},
    {"algoritmo": "Hill Climbing", "familia": "Local", "color": "#d97706", "tiempo": "Iteraciones locales", "espacio": "O(1)", "optimo": "No (máximos locales)"},
    {"algoritmo": "Recocido Simulado", "familia": "Local", "color": "#d97706", "tiempo": "Controlado por temperatura", "espacio": "O(1)", "optimo": "Probabilístico"},
    {"algoritmo": "Minimax + αβ", "familia": "Adversarial", "color": "#e11d48", "tiempo": "O(b^(m/2)) con poda ideal", "espacio": "O(b·m)", "optimo": "Sí (evaluación perfecta)"}
]

LEYENDA_TABLA = (
    "b = factor de ramificación · d = profundidad de la solución más cercana · m = profundidad máxima · "
    "C* = costo de la solución óptima · ε = costo mínimo de una acción. A* es exponencial en el peor caso, "
    "pero con una buena heurística el costo real depende de qué tan buena es h(n)."
)

# Historia de los algoritmos de búsqueda (complemento de investigación)
HISTORIA = [
    {
        "anio": "1950",
        "icono": "fa-chess",
        "hecho": "Claude Shannon publica 'Programar un computador para jugar ajedrez': nace Minimax aplicado a juegos."
    },
    {
        "anio": "1956",
        "icono": "fa-route",
        "hecho": "Edsger Dijkstra crea su algoritmo de caminos mínimos; John McCarthy formula la poda Alfa-Beta en Dartmouth."
    },
    {
        "anio": "1968",
        "icono": "fa-robot",
        "hecho": "Hart, Nilsson y Raphael publican A* en el SRI, para planificar rutas del robot Shakey."
    },
    {
        "anio": "1997",
        "icono": "fa-chess-king",
        "hecho": "Deep Blue (IBM) vence a Kasparov con búsqueda Alfa-Beta a ~200 millones de posiciones por segundo."
    },
    {
        "anio": "2016",
        "icono": "fa-brain",
        "hecho": "AlphaGo (DeepMind) vence a Lee Sedol combinando MCTS con redes neuronales profundas."
    }
]

# Aplicaciones reales (complemento de investigación)
APLICACIONES = [
    {
        "icono": "fa-map-location-dot",
        "lugar": "GPS y mapas (Google Maps, Waze)",
        "detalle": "Variantes de Dijkstra/A* sobre grafos de millones de nodos con tráfico en tiempo real."
    },
    {
        "icono": "fa-gamepad",
        "lugar": "Videojuegos",
        "detalle": "Los NPCs calculan rutas con A* sobre mallas de navegación en pocos milisegundos."
    },
    {
        "icono": "fa-robot",
        "lugar": "Robótica y almacenes (Amazon)",
        "detalle": "Brazos y carros autónomos planifican movimiento con A* y planificadores tipo RRT."
    },
    {
        "icono": "fa-cube",
        "lugar": "Puzzles (cubo de Rubik)",
        "detalle": "El 'número de Dios' (20 movimientos) se demostró con IDA* entre 43 quintillones de estados."
    },
    {
        "icono": "fa-calendar-check",
        "lugar": "Horarios y planificación (CSP)",
        "detalle": "Universidades y aerolíneas asignan horarios con Backtracking y propagación de restricciones."
    },
    {
        "icono": "fa-truck-fast",
        "lugar": "Logística e industria",
        "detalle": "Rutas de entrega y diseño de procesos con búsqueda local: Tabú, Recocido Simulado y Genéticos."
    }
]

FUENTES = (
    "Taxonomía clásica basada en Russell & Norvig — Artificial Intelligence: A Modern Approach (AIMA), "
    "complementada con Shannon (1950), Hart, Nilsson & Raphael (1968) e investigación propia."
)


# =========================================================================
# FUNCIONES DE ACCESO USADAS POR app.py
# =========================================================================
def obtener_info_algoritmos():
    """
    Retorna la información investigada de los incisos (a), (b), (c) y (d):
    definición, criterios de evaluación, elementos, ejemplo y clasificación.
    """
    return {
        "definicion": DEFINICION,
        "criterios": CRITERIOS_EVALUACION,
        "elementos": ELEMENTOS,
        "ejemplo": EJEMPLO,
        "intro_clasificacion": INTRO_CLASIFICACION,
        "clasificacion": CLASIFICACION_BUSQUEDA,
        "fichas": FICHAS_ALGORITMOS
    }


def obtener_infografia():
    """
    Retorna los datos de la infografía (inciso e): taxonomía multi-criterio,
    guía de selección, tabla comparativa, historia y aplicaciones reales.
    """
    return {
        "titulo": "Clasificación de Algoritmos de Búsqueda",
        "subtitulo": "Un mismo algoritmo puede pertenecer a varias familias a la vez: aquí se clasifica por criterios independientes que se combinan entre sí.",
        "dimensiones": CRITERIOS_EVALUACION,
        "criterios": CLASIFICACION_BUSQUEDA,
        "guia": GUIA_SELECCION,
        "tabla": TABLA_COMPARATIVA,
        "leyenda": LEYENDA_TABLA,
        "historia": HISTORIA,
        "aplicaciones": APLICACIONES,
        "fuentes": FUENTES
    }
