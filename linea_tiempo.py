"""
Módulo: Línea de Tiempo de la Inteligencia Artificial
Contiene los 10 hitos históricos fundamentales desde 1950 hasta la actualidad,
con detalles cronológicos, citas y curiosidades históricas.
"""

HITOS_TIMELINE = [
    {
        "id": 1,
        "periodo": "1950s",
        "fecha": "1950 - 1956",
        "titulo": "Nacimiento y Pioneros de la IA",
        "icono": "fa-brain",
        "color": "#2563eb",
        "imagen": "https://www.muycomputerpro.com/wp-content/uploads/2017/12/gartner-inteligencia-artificial.jpg",
        "hitos": [
            "1950 - Alan Turing publica 'Computing Machinery and Intelligence' y formula el célebre Test de Turing.",
            "1956 - Conferencia de Dartmouth organizada por John McCarthy, Marvin Minsky, Nathaniel Rochester y Claude Shannon; se acuña oficialmente el término 'Inteligencia Artificial'."
        ],
        "desc": "Alan Turing propuso un criterio empírico de conducta conversacional para evaluar si una máquina puede pensar. Pocos años después, el taller de Dartmouth sentó las bases fundacionales de la disciplina como campo formal de estudio.",
        "curiosidad": "A la Conferencia de Dartmouth de 1956 solo asistieron 10 investigadores en persona, pero sus postulados definieron el rumbo de la computación cognitiva durante las siguientes tres décadas."
    },
    {
        "id": 2,
        "periodo": "1960s",
        "fecha": "1966",
        "titulo": "ELIZA: El Primer Chatbot de la Historia",
        "icono": "fa-comments",
        "color": "#0284c7",
        "imagen": "https://upload.wikimedia.org/wikipedia/commons/7/79/ELIZA_conversation.png",
        "hitos": [
            "1966 - Joseph Weizenbaum crea ELIZA en el Laboratorio de IA del MIT.",
            "Implementación del script 'DOCTOR' simulando un terapeuta rogeriano."
        ],
        "desc": "ELIZA operaba mediante correspondencia de patrones de palabras clave y reglas de sustitución sintáctica simple. A pesar de su absoluta ausencia de comprensión o memoria interna, provocó que los usuarios le atribuyeran sentimientos e intenciones genuinas ('Efecto ELIZA').",
        "curiosidad": "Weizenbaum quedó tan desconcertado por el apego emocional real que su propia secretaria desarrolló hacia el programa que dedicó el resto de su carrera a advertir sobre los peligros del exceso de confianza en la tecnología."
    },
    {
        "id": 3,
        "periodo": "1970s",
        "fecha": "1974 - 1980",
        "titulo": "El Primer Invierno de la IA",
        "icono": "fa-snowflake",
        "color": "#0891b2",
        "imagen": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=600&auto=format&fit=crop",
        "hitos": [
            "1973 - Publicación del crítico 'Informe Lighthill' en el Reino Unido.",
            "Recorte drástico de presupuestos gubernamentales de DARPA y agencias internacionales."
        ],
        "desc": "Las promesas desmesuradas de los pioneros chocaron contra la cruda realidad: la capacidad de cálculo y la memoria de los ordenadores de la época eran insuficientes para abordar problemas de escalabilidad combinatoria y procesamiento de lenguaje.",
        "curiosidad": "Para sobrevivir al invierno financiero, los investigadores debieron evitar el uso de la frase 'inteligencia artificial' y rebautizar sus proyectos como 'sistemas adaptativos', 'algoritmos heurísticos' o 'ciencias computacionales avanzadas'."
    },
    {
        "id": 4,
        "periodo": "1980s",
        "fecha": "1980 - 1987",
        "titulo": "Auge de los Sistemas Expertos y Backpropagation",
        "icono": "fa-diagram-project",
        "color": "#0d9488",
        "imagen": "https://upload.wikimedia.org/wikipedia/commons/e/e5/DEC_VAX-11_780_1.jpg",
        "hitos": [
            "Éxito comercial de sistemas como MYCIN (diagnóstico infeccioso) y XCON/R1 en Digital Equipment Corporation.",
            "1986 - David Rumelhart, Geoffrey Hinton y Ronald Williams popularizan el algoritmo de Retropropagación (Backpropagation) para redes multicapa."
        ],
        "desc": "Las industrias adoptaron motores de inferencia simbólica basados en reglas lógicas 'SI... ENTONCES...'. Simultáneamente, el redescubrimiento de la retropropagación demostró que las redes neuronales podían aprender representaciones internas complejas.",
        "curiosidad": "El sistema experto XCON ahorraba a la corporación DEC aproximadamente 25 millones de dólares anuales en errores de ensamblaje de hardware."
    },
    {
        "id": 5,
        "periodo": "1990s",
        "fecha": "1997",
        "titulo": "Deep Blue vs Garry Kasparov",
        "icono": "fa-chess-king",
        "color": "#16a34a",
        "imagen": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Kasparov_Deep_Blue_1997.jpg",
        "hitos": [
            "Mayo de 1997 - La supercomputadora Deep Blue de IBM vence al campeón del mundo Garry Kasparov (3½ a 2½).",
            "Cálculo paralelo de hasta 200 millones de posiciones por segundo con chips aceleradores dedicados."
        ],
        "desc": "El histórico enfrentamiento marcó el momento en que una máquina superó el pináculo del ingenio táctico humano en ajedrez. Deep Blue combinó búsqueda heurística minimax con poda alfa-beta y bases de datos maestras de aperturas y finales.",
        "curiosidad": "Kasparov insinuó que hubo intervención de grandes maestros humanos detrás de la máquina tras la partida 2. Meses después de la victoria histórica, IBM desmontó permanentemente la supercomputadora."
    },
    {
        "id": 6,
        "periodo": "2000s",
        "fecha": "2000 - 2009",
        "titulo": "El Despegue del Machine Learning Estadístico",
        "icono": "fa-chart-line",
        "color": "#ca8a04",
        "imagen": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&auto=format&fit=crop",
        "hitos": [
            "2006 - Geoffrey Hinton publica métodos eficientes para entrenar Redes de Creencia Profunda y populariza el concepto 'Deep Learning'.",
            "2009 - La investigadora Fei-Fei Li y su equipo en Stanford crean ImageNet, recopilando más de 14 millones de imágenes jerarquizadas."
        ],
        "desc": "La comunidad científica abandonó la programación lógica deductiva y adoptó el aprendizaje inductivo basado en minería masiva de datos y modelos probabilísticos como SVMs, Random Forests y redes bayesianas.",
        "curiosidad": "ImageNet se financió en sus inicios con micro-trabajos en Amazon Mechanical Turk, donde decenas de miles de voluntarios etiquetaron millones de fotos a mano."
    },
    {
        "id": 7,
        "periodo": "2010s",
        "fecha": "2012 - 2016",
        "titulo": "Revolución del Deep Learning y AlphaGo",
        "icono": "fa-network-wired",
        "color": "#ea580c",
        "imagen": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Floor_Board_-_Go_%28Baduk_-_Weiqi%29.jpg",
        "hitos": [
            "2012 - AlexNet pulveriza el récord del reto ImageNet empleando GPUs NVIDIA.",
            "2016 - AlphaGo de Google DeepMind vence 4-1 a Lee Sedol, legendario campeón mundial de Go."
        ],
        "desc": "La concurrencia de tres factores (grandes volúmenes de datos, arquitecturas profundas y aceleración por GPUs) detonó la era moderna del Deep Learning. El juego milenario de Go, considerado imposible de calcular por computadoras, fue dominado mediante redes de valor, redes de políticas y aprendizaje por refuerzo.",
        "curiosidad": "En la segunda partida contra Lee Sedol, AlphaGo ejecutó el 'Movimiento 37', una jugada tan insólita que los comentaristas creyeron que era un fallo, pero que demostró ser una maniobra de intuición estratégica deslumbrante."
    },
    {
        "id": 8,
        "periodo": "2020s",
        "fecha": "2020 - 2022",
        "titulo": "GPT y la Explosión de la IA Generativa",
        "icono": "fa-robot",
        "color": "#dc2626",
        "imagen": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&auto=format&fit=crop",
        "hitos": [
            "2020 - OpenAI presenta GPT-3 con 175 mil millones de parámetros.",
            "2022 - Surgimiento de DALL-E 2, Midjourney y Stable Diffusion.",
            "Noviembre 2022 - Lanzamiento de ChatGPT, alcanzando 100 millones de usuarios activos en 60 días."
        ],
        "desc": "El escalamiento masivo de modelos autorregresivos transformó a la IA de una disciplina técnica a un fenómeno cultural cotidiano global. La capacidad de redactar prosa pulida, escribir código y crear arte fotorrealista cambió la relación de la humanidad con la tecnología.",
        "curiosidad": "ChatGPT se convirtió en la aplicación de consumo de más rápido crecimiento en la historia de Internet, superando con creces las marcas de adopción de TikTok e Instagram."
    },
    {
        "id": 9,
        "periodo": "2023 - 2024",
        "fecha": "2023 - 2024",
        "titulo": "Multimodalidad y Democratización de Código Abierto",
        "icono": "fa-photo-film",
        "color": "#9333ea",
        "imagen": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=600&auto=format&fit=crop",
        "hitos": [
            "2023 - Lanzamiento de GPT-4 (razonamiento multimodal y superación de exámenes profesionales).",
            "2024 - Aparición de Sora (generación de video coherente de alta fidelidad) y Claude 3.",
            "Consolidación de modelos de pesos abiertos de clase mundial como la familia Llama 3 de Meta y Mistral."
        ],
        "desc": "La frontera tecnológica integró modalidades sensoriales fluidas (visión, voz, texto y video simultáneos) en tiempo real. Simultáneamente, la comunidad de código abierto demostró que modelos abiertos podían competir de cerca con sistemas cerrados propietarios.",
        "curiosidad": "En 2024 se logró por primera vez que un modelo de pesos abiertos alcanzara puntuaciones en razonamiento matemático y programación equiparables a los modelos comerciales más avanzados del mundo."
    },
    {
        "id": 10,
        "periodo": "Hoy",
        "fecha": "2025 - Presente",
        "titulo": "Era de los Agentes Autónomos y Razonamiento Lógico Profundo",
        "icono": "fa-users-gear",
        "color": "#4f46e5",
        "imagen": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&auto=format&fit=crop",
        "hitos": [
            "Modelos con cadenas internas de razonamiento deductivo paso a paso (Chain-of-Thought / OpenAI o1).",
            "Despliegue masivo de enjambres de agentes autónomos con uso de herramientas y ejecución de código.",
            "Integración de inferencia local en chips NPU en computadoras personales y teléfonos inteligentes."
        ],
        "desc": "La inteligencia artificial transita de ser un oráculo pasivo que responde preguntas a convertirse en un agente activo que diseña software, audita sistemas de seguridad, orquesta flujos de trabajo científicos y colabora en equipos humanos.",
        "curiosidad": "Más del 50% del código nuevo producido en las empresas tecnológicas más grandes del mundo es ahora redactado o asistido en tiempo real por agentes inteligentes de IA."
    }
]

def obtener_hitos():
    """
    Retorna la lista completa de hitos cronológicos de la IA.
    """
    return HITOS_TIMELINE
