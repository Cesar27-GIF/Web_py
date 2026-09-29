"""
Módulo: Clasificación de la Inteligencia Artificial
Define los niveles fundamentales de capacidad (IA Débil, IA Fuerte y Superinteligencia),
así como la taxonomía funcional de Arend Hintze.
"""

CLASIFICACION_IA = [
    {
        "id": "debil",
        "tipo": "IA Débil (Narrow AI / Weak AI)",
        "subtitulo": "Especializada, Acotada y Operativa",
        "badge": "Dominante en la Actualidad",
        "badge_color": "success",
        "icono": "fa-microchip",
        "imagen_gdrive": "https://lh3.googleusercontent.com/d/1jZVDLHAzRrxibCM0HLydv8zUWFo4RKYU",
        "enlace_original": "https://drive.google.com/file/d/1jZVDLHAzRrxibCM0HLydv8zUWFo4RKYU/view?usp=sharing",
        "definicion": "Sistemas programados y entrenados para resolver de manera sobresaliente un conjunto cerrado de tareas bien delimitadas, sin poseer consciencia, empatía ni capacidad de extrapolación conceptual a otros dominios.",
        "caracteristicas": [
            "Diseñada para resolver una tarea o conjunto de tareas específicas de forma altamente eficiente.",
            "Carece de conciencia, intención o entendimiento general del contexto fuera de su dominio de entrenamiento.",
            "Opera bajo reglas lógicas fijas o modelos estadísticos ajustados con datos históricos específicos.",
            "Si se le pide resolver un problema fuera de su arquitectura, falla completamente sin capacidad de adaptación.",
            "Ejemplos reales: Motores de búsqueda de Google, asistentes Siri/Alexa, filtros de spam, sistemas de recomendación de Netflix/Spotify y reconocimiento de matrículas."
        ],
        "limites": "Incapaz de transferir sentido común o experiencia acumulada a problemas radicalmente distintos sin reingeniería."
    },
    {
        "id": "fuerte",
        "tipo": "IA Fuerte (AGI / Artificial General Intelligence)",
        "subtitulo": "General, Transversal e Igual a la Mente Humana",
        "badge": "En Investigación Activa de Frontera",
        "badge_color": "warning",
        "icono": "fa-brain",
        "imagen_gdrive": "https://lh3.googleusercontent.com/d/1fhfEnGbBcm2EluBYa3Omvr7Ygj9hO8s_",
        "enlace_original": "https://drive.google.com/file/d/1fhfEnGbBcm2EluBYa3Omvr7Ygj9hO8s_/view?usp=sharing",
        "definicion": "Sistemas teóricos que emulan la capacidad cognitiva universal humana, capaces de formular juicios, abstraer ideas, resolver dilemas imprevistos y aprender disciplinas dispares de manera autónoma.",
        "caracteristicas": [
            "Sistemas con capacidad cognitiva general comparable o equivalente a la mente humana en todas las facetas intelectuales.",
            "Capaces de aprender, razonar, abstraer, planificar y aplicar conocimientos en múltiples dominios sin supervisión ni reentrenamiento.",
            "Poseen adaptabilidad profunda ante la incertidumbre, sentido común emergente y comprensión semántica real.",
            "Capacidad de autoreflexión, análisis crítico de sus propios errores y automejora iterativa.",
            "Ejemplos: Modelos de razonamiento de frontera, arquitecturas agénticas universales y proyectos de investigación en DeepMind y OpenAI."
        ],
        "limites": "Representa el objetivo supremo de la ciencia informática moderna; aún no se ha alcanzado de manera definitiva."
    },
    {
        "id": "super",
        "tipo": "Superinteligencia Artificial (ASI / Artificial Superintelligence)",
        "subtitulo": "Trascendencia Absoluta sobre la Capacidad Intelectual Humana",
        "badge": "Frontera Teórica / Futuro Hipotético",
        "badge_color": "danger",
        "icono": "fa-atom",
        "imagen_gdrive": "https://lh3.googleusercontent.com/d/15Tg-kPwIjICEVy7sEP0kNG8G2ZszpQXC",
        "enlace_original": "https://drive.google.com/file/d/15Tg-kPwIjICEVy7sEP0kNG8G2ZszpQXC/view?usp=sharing",
        "definicion": "Entidad algorítmica hipotética cuyo intelecto superaría por órdenes de magnitud al de los cerebros humanos más brillantes combinados, manifestando una capacidad casi ilimitada de invención científica y resolución de problemas.",
        "caracteristicas": [
            "Inteligencia que excede exponencialmente la capacidad combinada de toda la especie humana en todos los campos científicos y filosóficos.",
            "Capaz de realizar saltos conceptuales en física, biología molecular, computación cuántica y sociología en fracciones de segundo.",
            "Dona de una capacidad de autorreprogramación y optimización recursiva ultrarrápida (explosión de inteligencia postulada por I.J. Good).",
            "Plantea los máximos debates éticos y de supervivencia existencial sobre alineación de valores humanos, seguridad y control.",
            "Ejemplos: Construcciones teóricas postuladas por Nick Bostrom, Max Tegmark y centros de investigación de seguridad de la IA."
        ],
        "limites": "Desconocimiento absoluto sobre si sus objetivos finales permanecerán alineados con el bienestar y preservación de la humanidad."
    }
]

# Taxonomía funcional complementaria de Arend Hintze
NIVELES_FUNCIONALES = [
    {
        "nombre": "1. Máquinas Reactivas",
        "desc": "No almacenan recuerdos ni usan experiencias pasadas para decidir en tiempo real.",
        "ejemplo": "Deep Blue de IBM calculando jugadas en tiempo presente sin memoria de partidos anteriores.",
        "icono": "fa-bolt"
    },
    {
        "nombre": "2. Memoria Limitada",
        "desc": "Registran información del pasado reciente para tomar decisiones a corto plazo.",
        "ejemplo": "Vehículos autónomos (Tesla/Waymo) monitoreando la trayectoria reciente de peatones.",
        "icono": "fa-database"
    },
    {
        "nombre": "3. Teoría de la Mente",
        "desc": "Comprenderían emociones, intenciones y creencias humanas para interactuar empáticamente.",
        "ejemplo": "En desarrollo experimental; interacción socio-robótica adaptativa.",
        "icono": "fa-heart-pulse"
    },
    {
        "nombre": "4. Autoconsciencia",
        "desc": "Consciencia de su propia existencia, sentimientos y estados cognitivos internos.",
        "ejemplo": "Hipotética etapa final de la evolución de la inteligencia sintética.",
        "icono": "fa-sparkles"
    }
]

def obtener_clasificacion():
    """
    Retorna la lista de clasificaciones principales de IA.
    """
    return CLASIFICACION_IA

def obtener_niveles_funcionales():
    """
    Retorna la taxonomía funcional de Hintze.
    """
    return NIVELES_FUNCIONALES
