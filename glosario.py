"""
Módulo: Glosario de Inteligencia Artificial
Contiene los 20 conceptos técnicos organizados por nivel de uso,
así como funciones de búsqueda y filtrado.
"""

TERMINOS = [
    # Muy Común
    {
        "id": 1,
        "nivel": "Muy Común",
        "nivel_code": "comun",
        "termino": "Inteligencia Artificial (IA)",
        "categoria": "Fundamentos",
        "def": "Disciplina sistémica de las ciencias de la computación enfocada en diseñar algoritmos capaces de abstraer modelos del mundo real, resolver problemas de optimización estocástica y simular funciones cognitivas avanzadas como el razonamiento y la toma de decisiones.",
        "imagen": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=500&auto=format&fit=crop",
        "aplicacion": "Diagnósticos asistidos, conducción autónoma y motores de recomendación."
    },
    {
        "id": 2,
        "nivel": "Muy Común",
        "nivel_code": "comun",
        "termino": "Aprendizaje Automático (Machine Learning)",
        "categoria": "Modelado",
        "def": "Subcampo cuantitativo enfocado en la construcción de modelos matemáticos cuyos parámetros se ajustan iterativamente mediante algoritmos de optimización numérico-estadística a partir de conjuntos de datos de entrenamiento.",
        "imagen": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500&auto=format&fit=crop",
        "aplicacion": "Detección de fraudes financieros, predicción climática y segmentación de clientes."
    },
    {
        "id": 3,
        "nivel": "Muy Común",
        "nivel_code": "comun",
        "termino": "Aprendizaje Profundo (Deep Learning)",
        "categoria": "Redes Neuronales",
        "def": "Metodología basada en la jerarquización de representaciones abstractas mediante redes neuronales profundas de múltiples capas que aplican transformaciones compuestas no lineales sucesivas.",
        "imagen": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&auto=format&fit=crop",
        "aplicacion": "Reconocimiento de voz, visión artificial y síntesis de video en alta definición."
    },
    {
        "id": 4,
        "nivel": "Muy Común",
        "nivel_code": "comun",
        "termino": "Procesamiento del Lenguaje Natural (NLP)",
        "categoria": "Lingüística Computacional",
        "def": "Área de intersección entre lingüística computacional y modelado probabilístico orientada a descomponer la ambigüedad morfosintáctica y semántica del lenguaje humano para su comprensión y generación.",
        "imagen": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500&auto=format&fit=crop",
        "aplicacion": "Traductores automáticos, análisis de sentimientos y corrección gramatical inteligente."
    },
    {
        "id": 5,
        "nivel": "Muy Común",
        "nivel_code": "comun",
        "termino": "Visión por Computador (Computer Vision)",
        "categoria": "Percepción",
        "def": "Dominio enfocado en la extracción de invariantes espaciales y descriptores semánticos a partir de matrices de píxeles para segmentación, detección de objetos y reconstrucción tridimensional de escenas.",
        "imagen": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500&auto=format&fit=crop",
        "aplicacion": "Reconocimiento facial de seguridad, inspección industrial automatizada y resonancias médicas."
    },

    # Poco Común
    {
        "id": 6,
        "nivel": "Poco Común",
        "nivel_code": "poco_comun",
        "termino": "Redes Neuronales Artificiales (ANN)",
        "categoria": "Arquitectura",
        "def": "Grafos dirigidos ponderados organizados en capas de nodos que emplean funciones de activación no lineales y el algoritmo de backpropagation para lograr la aproximación universal de funciones matemáticas.",
        "imagen": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500&auto=format&fit=crop",
        "aplicacion": "Modelado de series temporales complejas y clasificación de señales biomédicas."
    },
    {
        "id": 7,
        "nivel": "Poco Común",
        "nivel_code": "poco_comun",
        "termino": "Overfitting (Sobreajuste)",
        "categoria": "Optimización",
        "def": "Fenómeno de alta varianza estadística donde la función de pérdida decrece drásticamente en entrenamiento pero se dispara en datos de validación debido a la memorización indeseada de ruido estocástico.",
        "imagen": "https://images.unsplash.com/photo-1543286386-713bdd548da4?w=500&auto=format&fit=crop",
        "aplicacion": "Se combate con regularización (L1/L2), Dropout y aumento de datos sintéticos."
    },
    {
        "id": 8,
        "nivel": "Poco Común",
        "nivel_code": "poco_comun",
        "termino": "Fine-Tuning (Ajuste Fino)",
        "categoria": "Transfer Learning",
        "def": "Estrategia de aprendizaje por transferencia donde los pesos de una red neuronal previamente entrenada sobre un corpus colosal se congelan parcialmente y se reajustan con un conjunto de datos específico.",
        "imagen": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=500&auto=format&fit=crop",
        "aplicacion": "Especialización de LLMs en jurisprudencia, medicina o manuales corporativos."
    },
    {
        "id": 9,
        "nivel": "Poco Común",
        "nivel_code": "poco_comun",
        "termino": "Sesgo Algorítmico (Algorithmic Bias)",
        "categoria": "Ética y Datos",
        "def": "Desviación sistemática e injusta en las decisiones predictivas originada por asimetrías muestrales en los datos de entrenamiento, correlaciones espurias o formulaciones erróneas de la función de coste.",
        "imagen": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=500&auto=format&fit=crop",
        "aplicacion": "Auditorías de equidad en algoritmos de preselección de empleo y concesión de hipotecas."
    },
    {
        "id": 10,
        "nivel": "Poco Común",
        "nivel_code": "poco_comun",
        "termino": "Aprendizaje por Refuerzo (Reinforcement Learning)",
        "categoria": "Paradigmas",
        "def": "Paradigma fundamentado en Procesos de Decisión de Markov donde un agente interactúa dinámicamente con un entorno estocástico mediante acciones que buscan maximizar una señal de recompensa escalar acumulada.",
        "imagen": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=500&auto=format&fit=crop",
        "aplicacion": "Control de robots bípedos, optimización de redes energéticas y juegos de estrategia (Go, Chess)."
    },

    # En Prueba
    {
        "id": 11,
        "nivel": "En Prueba",
        "nivel_code": "prueba",
        "termino": "RAG (Retrieval-Augmented Generation)",
        "categoria": "Arquitectura Híbrida",
        "def": "Arquitectura que conecta bases de datos vectoriales indexadas con modelos generativos para inyectar fragmentos de conocimiento factual verificado en el prompt antes de generar la respuesta final.",
        "imagen": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=500&auto=format&fit=crop",
        "aplicacion": "Sistemas de consulta jurídica sobre jurisprudencia viva y soporte técnico bancario privado."
    },
    {
        "id": 12,
        "nivel": "En Prueba",
        "nivel_code": "prueba",
        "termino": "Agente Autónomo de IA",
        "categoria": "Sistemas Autónomos",
        "def": "Sistema con orquestación modular que combina un modelo fundacional como motor de razonamiento, memoria episódica, capacidad de autocrítica y ejecución automatizada de APIs y herramientas externas.",
        "imagen": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=500&auto=format&fit=crop",
        "aplicacion": "Depuración automática de software, investigación documental de mercado y flujos de trabajo en DevOps."
    },
    {
        "id": 13,
        "nivel": "En Prueba",
        "nivel_code": "prueba",
        "termino": "Alucinación en IA (AI Hallucination)",
        "categoria": "Comportamiento del Modelo",
        "def": "Divergencia factual inherente a modelos autorregresivos donde el sistema sintetiza secuencias de texto con alta fluidez sintáctica y convicción aparente pero sin correspondencia con la realidad verificable.",
        "imagen": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&auto=format&fit=crop",
        "aplicacion": "Se mitiga con verificación formal, muestreo de temperatura baja y técnicas RAG."
    },
    {
        "id": 14,
        "nivel": "En Prueba",
        "nivel_code": "prueba",
        "termino": "Prompt Engineering",
        "categoria": "Interacción Humano-IA",
        "def": "Metodología sistemática de diseño y formulación de restricciones contextuales, cadenas de pensamiento (Chain-of-Thought) e instrucciones estructuradas para guiar el espacio latente de un modelo hacia respuestas óptimas.",
        "imagen": "https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=500&auto=format&fit=crop",
        "aplicacion": "Optimización de outputs para pipelines de desarrollo y generación guiada de código fuente."
    },
    {
        "id": 15,
        "nivel": "En Prueba",
        "nivel_code": "prueba",
        "termino": "IA Multimodal",
        "categoria": "Frontera de Percepción",
        "def": "Modelos con espacios de incrustación (embeddings) compartidos o proyectados que procesan, alinean y generan simultáneamente múltiples modalidades sensoriales como texto, imágenes satelitales, audio y video.",
        "imagen": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500&auto=format&fit=crop",
        "aplicacion": "Análisis simultáneo de audio y video en telemedicina, inspección de infraestructura y subtitulado dinámico."
    },

    # Apenas Apareciendo
    {
        "id": 16,
        "nivel": "Apenas Apareciendo",
        "nivel_code": "emergente",
        "termino": "Transformers (Mecanismos de Atención)",
        "categoria": "Arquitectura de Frontera",
        "def": "Arquitectura neural basada en mecanismos de autoatención multicabeza (Self-Attention) que procesa secuencias en paralelo eliminando las dependencias secuenciales lentas de las redes recurrentes tradicionales.",
        "imagen": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=500&auto=format&fit=crop",
        "aplicacion": "Columna vertebral de todos los modelos de lenguaje modernos (GPT, BERT, Claude, Llama)."
    },
    {
        "id": 17,
        "nivel": "Apenas Apareciendo",
        "nivel_code": "emergente",
        "termino": "Tokenización y Espacios Latentes",
        "categoria": "Procesamiento de Entrada",
        "def": "Algoritmos de segmentación subpalabra (BPE, WordPiece) que descomponen entradas de datos en identificadores numéricos discretos y los mapean a espacios vectoriales continuos de alta dimensionalidad.",
        "imagen": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=500&auto=format&fit=crop",
        "aplicacion": "Compresión semántica e ingesta de datos para modelos de lenguaje y visión."
    },
    {
        "id": 18,
        "nivel": "Apenas Apareciendo",
        "nivel_code": "emergente",
        "termino": "LLM (Modelos Grandes de Lenguaje)",
        "categoria": "Modelos Fundacionales",
        "def": "Redes neuronales autorregresivas a escala masiva (miles de millones de parámetros) preentrenadas sobre corpus masivos que exhiben propiedades emergentes como razonamiento deductivo y resolución de tareas no vistas.",
        "imagen": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=500&auto=format&fit=crop",
        "aplicacion": "Copilotos de programación, asistentes analíticos, síntesis científica y traducción cruzada."
    },
    {
        "id": 19,
        "nivel": "Apenas Apareciendo",
        "nivel_code": "emergente",
        "termino": "IA Generativa (Modelos de Difusión y VAEs)",
        "categoria": "Síntesis Creativa",
        "def": "Familia de modelos probabilísticos avanzados diseñados para modelar la distribución subyacente de datos reales y sintetizar nuevas instancias originales de alta fidelidad como audio, video, código y química sintética.",
        "imagen": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=500&auto=format&fit=crop",
        "aplicacion": "Diseño de fármacos sintéticos, generación cinematográfica sintética y arquitectura paramétrica."
    },
    {
        "id": 20,
        "nivel": "Apenas Apareciendo",
        "nivel_code": "emergente",
        "termino": "AGI (Inteligencia Artificial General)",
        "categoria": "Frontera Teórica",
        "def": "Umbral hipotético que describe un sistema artificial dotado de adaptabilidad cognitiva transversal equivalente o superior a la humana, capaz de razonar, aprender y resolver cualquier problema intelectual sin reentrenamiento previo.",
        "imagen": "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=500&auto=format&fit=crop",
        "aplicacion": "Aceleración científica de frontera en física teórica, biomedicina curativa y gobernanza global del clima."
    }
]

def obtener_terminos(query: str = '', nivel_filtro: str = ''):
    """
    Filtra la lista de términos según término de búsqueda y nivel de uso.
    """
    query = (query or '').strip().lower()
    nivel_filtro = (nivel_filtro or '').strip().lower()

    filtrados = TERMINOS

    if nivel_filtro:
        filtrados = [t for t in filtrados if t['nivel_code'] == nivel_filtro]

    if query:
        filtrados = [
            t for t in filtrados
            if query in t['termino'].lower()
            or query in t['def'].lower()
            or query in t['nivel'].lower()
            or query in t.get('categoria', '').lower()
            or query in t.get('aplicacion', '').lower()
        ]

    return filtrados

def obtener_estadisticas_glosario():
    """
    Retorna métricas cuantitativas sobre el catálogo del glosario.
    """
    return {
        "total": len(TERMINOS),
        "comun": len([t for t in TERMINOS if t['nivel_code'] == 'comun']),
        "poco_comun": len([t for t in TERMINOS if t['nivel_code'] == 'poco_comun']),
        "prueba": len([t for t in TERMINOS if t['nivel_code'] == 'prueba']),
        "emergente": len([t for t in TERMINOS if t['nivel_code'] == 'emergente'])
    }
