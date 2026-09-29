"""
Módulo: Machine Learning (Aprendizaje Automático)
Contiene la base conceptual, los paradigmas, el ciclo de vida de un modelo de ML,
y un ejemplo práctico interactivo completamente funcional:
Un clasificador probabilístico de Spam / Phishing implementado en Python puro.
"""

import re
import math
from typing import Dict, List, Any, Tuple

# ==============================================================================
# 1. BASE DE CONOCIMIENTO TEÓRICA SOBRE MACHINE LEARNING
# ==============================================================================

INFO_MACHINE_LEARNING = {
    "titulo": "Fundamentos y Paradigmas del Machine Learning",
    "definicion": (
        "El Machine Learning (Aprendizaje Automático) es una rama de la Inteligencia Artificial "
        "que dota a los ordenadores de la capacidad de aprender y mejorar a partir de la experiencia "
        "y los datos, sin ser programados explícitamente mediante reglas deterministas fijas. "
        "Formalmente, como enunció Tom Mitchell (1997): 'Se dice que un programa de computadora aprende "
        "de la experiencia E con respecto a una clase de tareas T y una medida de desempeño P, "
        "si su desempeño en las tareas de T, medido por P, mejora con la experiencia E'."
    ),
    "paradigmas": [
        {
            "id": "supervisado",
            "nombre": "Aprendizaje Supervisado",
            "icono": "fa-user-graduate",
            "color": "#0284c7",
            "descripcion": (
                "El modelo se entrena sobre un conjunto de datos etiquetado con pares de entrada y salida "
                "(X, y). Su meta es aprender una función de mapeo que generalice con precisión sobre nuevos datos no observados."
            ),
            "tipos": ["Clasificación (salida discreta: spam/no spam)", "Regresión (salida continua: precios, temperatura)"],
            "algoritmos": ["Regresión Lineal/Logística", "Árboles de Decisión y Random Forest", "Support Vector Machines (SVM)", "Redes Neuronales Densas"],
            "ejemplo_uso": "Predecir si una transacción bancaria es legítima o fraudulenta a partir de patrones históricos etiquetados."
        },
        {
            "id": "no_supervisado",
            "nombre": "Aprendizaje No Supervisado",
            "icono": "fa-network-wired",
            "color": "#0d9488",
            "descripcion": (
                "El algoritmo recibe datos sin etiquetas ni objetivos predefinidos (solo X). Debe descubrir "
                "por sí mismo estructuras ocultas, agrupaciones naturales, densidades o patrones subyacentes."
            ),
            "tipos": ["Clustering (agrupamiento)", "Reducción de Dimensionalidad (PCA, t-SNE)", "Detección de Anomalías"],
            "algoritmos": ["K-Means", "DBSCAN", "Análisis de Componentes Principales (PCA)", "Autoencoders"],
            "ejemplo_uso": "Segmentación automática de clientes de comercio electrónico según hábitos de compra afines."
        },
        {
            "id": "refuerzo",
            "nombre": "Aprendizaje por Refuerzo",
            "icono": "fa-gamepad",
            "color": "#7c3aed",
            "descripcion": (
                "Un agente autónomo aprende a interactuar con un entorno dinámico mediante ensayo y error. "
                "Recibe recompensas (+1) o penalizaciones (-1) según sus acciones, con la meta de maximizar la recompensa total acumulada."
            ),
            "tipos": ["Basado en Valor (Q-Learning)", "Basado en Políticas (Policy Gradients)", "Actor-Critic (PPO, DDPG)"],
            "algoritmos": ["Q-Learning", "Deep Q-Networks (DQN)", "Proximal Policy Optimization (PPO)", "Monte Carlo Tree Search"],
            "ejemplo_uso": "Navegación robótica en terrenos no explorados y superación de juegos de estrategia como Go y Ajedrez."
        }
    ],
    "pipeline": [
        {
            "paso": "1. Definición & Recolección",
            "desc": "Establecer la pregunta de negocio o problema científico y capturar datos históricos relevantes y representativos.",
            "icono": "fa-database"
        },
        {
            "paso": "2. Limpieza & EDA",
            "desc": "Tratar valores nulos, eliminar duplicados, analizar distribuciones y detectar outliers anómalos.",
            "icono": "fa-filter"
        },
        {
            "paso": "3. Feature Engineering",
            "desc": "Normalizar escalas, codificar variables categóricas (One-Hot) y crear variables predictoras de alto impacto.",
            "icono": "fa-sliders"
        },
        {
            "paso": "4. Train / Validation / Test",
            "desc": "Dividir los datos (ej. 70%-15%-15%) para prevenir el sobreajuste (overfitting) y validar la generalización real.",
            "icono": "fa-columns"
        },
        {
            "paso": "5. Entrenamiento & Ajuste",
            "desc": "Optimizar la función de pérdida mediante algoritmos numéricos como Descenso de Gradiente (SGD, Adam).",
            "icono": "fa-brain"
        },
        {
            "paso": "6. Evaluación Rigurosa",
            "desc": "Calcular métricas de rendimiento objetivas: Precisión, Recall, F1-Score, Curva ROC-AUC, Matriz de Confusión y RMSE.",
            "icono": "fa-chart-pie"
        },
        {
            "paso": "7. Despliegue & MLOps",
            "desc": "Empaquetar el modelo como API REST o microservicio y monitorear deriva de datos (data drift) en producción.",
            "icono": "fa-rocket"
        }
    ]
}

# ==============================================================================
# 2. EJEMPLO PRÁCTICO 1: CLASIFICADOR NAIVE BAYES EN PYTHON PURO
# ==============================================================================

# Dataset de entrenamiento sintético curado en español para detección de Spam / Phishing
DATASET_ENTRENAMIENTO = [
    # Mensajes SPAM / Phishing (Etiqueta: 'spam')
    ("¡Felicidades! Has ganado 1,000,000 de pesos en la lotería nacional. Reclama tu premio aquí urgente.", "spam"),
    ("Urgente: Tu cuenta bancaria ha sido bloqueada. Ingresa tu contraseña y clave de seguridad de inmediato.", "spam"),
    ("Gana dinero fácil y rápido trabajando desde casa. Sin inversión previa, haz clic en el enlace ahora.", "spam"),
    ("Préstamo express aprobado de inmediato con 0% de interés. Transfiere solo comisión de apertura.", "spam"),
    ("Oferta exclusiva por tiempo limitado: 90% de descuento en relojes de lujo y criptomonedas gratis.", "spam"),
    ("Alerta de seguridad: Detectamos un inicio de sesión no reconocido. Haz clic para verificar tus credenciales.", "spam"),
    ("Premio millonario garantizado. Envía tus datos personales y número de tarjeta para recibir la transferencia.", "spam"),
    ("¡Última oportunidad! Multiplica tus bitcoins en 24 horas garantizado con nuestra plataforma de inversión.", "spam"),
    ("Su paquete no pudo ser entregado. Pague la tasa de aduana de inmediato haciendo clic aquí.", "spam"),
    ("Gana un iPhone 15 Pro totalmente gratis respondiendo esta breve encuesta de 2 minutos.", "spam"),
    ("Actualice sus datos fiscales o su cuenta del SAT será suspendida de forma irrevocable hoy mismo.", "spam"),
    ("¡Promoción millonaria! Regalo sorpresa para usuarios leales, reclámalo antes de medianoche.", "spam"),

    # Mensajes LEGÍTIMOS / Ham (Etiqueta: 'ham')
    ("Hola profesor, le comparto el archivo con la tarea de Machine Learning correspondiente a la entrega final.", "ham"),
    ("Buenas tardes equipo, la reunión semanal de seguimiento se pospone para mañana a las 10:00 AM.", "ham"),
    ("¿A qué hora nos vemos hoy en la biblioteca para repasar los temas del examen de inteligencia artificial?", "ham"),
    ("Estimado alumno, le notificamos que su inscripción al curso de matemáticas aplicadas fue registrada con éxito.", "ham"),
    ("Hola mamá, ya llegué a la universidad. Te llamo por la tarde cuando termine las clases del laboratorio.", "ham"),
    ("Adjunto minuta del proyecto y el cronograma acordado en la junta directiva de esta mañana.", "ham"),
    ("Gracias por tu apoyo en la presentación de ayer, los profesores quedaron muy conformes con el prototipo.", "ham"),
    ("Recordatorio: La fecha límite para entregar el reporte de investigación sobre ética algorítmica es el viernes.", "ham"),
    ("Hola Carlos, ¿podrías enviarme por favor las diapositivas de la conferencia sobre redes neuronales?", "ham"),
    ("Confirmamos la recepción de tu comprobante de pago de colegiatura para el nuevo cuatrimestre escolar.", "ham"),
    ("Te comparto el enlace al repositorio de GitHub con el código fuente del proyecto Flask.", "ham"),
    ("Nos vemos a la hora del almuerzo en la cafetería central para platicar sobre el avance de la tesis.", "ham")
]

class ClasificadorSpamNaiveBayes:
    """
    Implementación ligera y didáctica de Naive Bayes Multinomial con Suavizado de Laplace
    escrita completamente en Python estándar sin dependencias externas.
    """

    def __init__(self):
        self.vocabulario = set()
        self.conteo_palabras_spam: Dict[str, int] = {}
        self.conteo_palabras_ham: Dict[str, int] = {}
        self.total_palabras_spam = 0
        self.total_palabras_ham = 0
        self.total_docs_spam = 0
        self.total_docs_ham = 0
        self.prior_spam = 0.5
        self.prior_ham = 0.5
        self._entrenar()

    def _tokenizar(self, texto: str) -> List[str]:
        # Normalizar a minúsculas y extraer tokens de palabras alfanuméricas
        palabras = re.findall(r'[a-záéíóúñ0-9]+', texto.lower())
        # Filtrar conectores muy comunes no informativos (stopwords básicas)
        stopwords = {'de', 'la', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'ha'}
        return [p for p in palabras if p not in stopwords and len(p) > 2]

    def _entrenar(self):
        for texto, etiqueta in DATASET_ENTRENAMIENTO:
            tokens = self._tokenizar(texto)
            for t in tokens:
                self.vocabulario.add(t)
                if etiqueta == 'spam':
                    self.conteo_palabras_spam[t] = self.conteo_palabras_spam.get(t, 0) + 1
                    self.total_palabras_spam += 1
                else:
                    self.conteo_palabras_ham[t] = self.conteo_palabras_ham.get(t, 0) + 1
                    self.total_palabras_ham += 1

            if etiqueta == 'spam':
                self.total_docs_spam += 1
            else:
                self.total_docs_ham += 1

        total_docs = self.total_docs_spam + self.total_docs_ham
        self.prior_spam = self.total_docs_spam / total_docs
        self.prior_ham = self.total_docs_ham / total_docs

    def predecir(self, texto: str) -> Dict[str, Any]:
        tokens = self._tokenizar(texto)
        if not tokens:
            return {
                "etiqueta": "INCIERTO",
                "es_spam": False,
                "probabilidad_spam": 50.0,
                "probabilidad_ham": 50.0,
                "tokens_analizados": [],
                "palabras_clave_spam": [],
                "explicacion": "El texto proporcionado no contiene suficientes palabras significativas para inferir una predicción confiable."
            }

        v_tam = len(self.vocabulario)
        # Log-verosimilitud inicial con el prior de cada clase
        log_prob_spam = math.log(self.prior_spam)
        log_prob_ham = math.log(self.prior_ham)

        palabras_clave_encontradas = []

        for t in tokens:
            # Suavizado de Laplace (Add-1 Smoothing)
            conteo_sp = self.conteo_palabras_spam.get(t, 0)
            p_w_dado_spam = (conteo_sp + 1) / (self.total_palabras_spam + v_tam)
            log_prob_spam += math.log(p_w_dado_spam)

            conteo_hm = self.conteo_palabras_ham.get(t, 0)
            p_w_dado_ham = (conteo_hm + 1) / (self.total_palabras_ham + v_tam)
            log_prob_ham += math.log(p_w_dado_ham)

            if conteo_sp > conteo_hm:
                palabras_clave_encontradas.append({
                    "palabra": t,
                    "relevancia_spam": round((conteo_sp + 1) / (conteo_hm + 1), 2)
                })

        # Convertir log-probabilidades a probabilidades relativas normalizadas (Softmax / Bayes)
        # Estabilidad numérica restando el máximo
        max_log = max(log_prob_spam, log_prob_ham)
        exp_spam = math.exp(log_prob_spam - max_log)
        exp_ham = math.exp(log_prob_ham - max_log)
        total_exp = exp_spam + exp_ham

        prob_spam_norm = (exp_spam / total_exp) * 100
        prob_ham_norm = (exp_ham / total_exp) * 100

        es_spam = prob_spam_norm >= 50.0
        etiqueta = "SPAM / FRAUDULENTO" if es_spam else "LEGÍTIMO (HAM)"

        # Ordenar palabras clave de spam más influyentes
        palabras_clave_encontradas.sort(key=lambda x: x["relevancia_spam"], reverse=True)

        return {
            "etiqueta": etiqueta,
            "es_spam": es_spam,
            "probabilidad_spam": round(prob_spam_norm, 1),
            "probabilidad_ham": round(prob_ham_norm, 1),
            "tokens_analizados": tokens,
            "palabras_clave_spam": [p["palabra"] for p in palabras_clave_encontradas[:5]],
            "explicacion": (
                f"El modelo evaluó {len(tokens)} palabras discriminantes. "
                f"La probabilidad asignada a contenido no deseado/fraudulento es del {round(prob_spam_norm, 1)}% "
                f"frente a un {round(prob_ham_norm, 1)}% de comunicación legítima."
            )
        }

# Instancia singleton del clasificador
_MODELO_SPAM = ClasificadorSpamNaiveBayes()

def clasificar_mensaje_spam(texto: str) -> Dict[str, Any]:
    """
    Función de inferencia que analiza un mensaje en tiempo real.
    """
    return _MODELO_SPAM.predecir(texto)

# ==============================================================================
# 3. EJEMPLO PRÁCTICO 2: CASO DE ESTUDIO DE REGRESIÓN (PRECIOS DE VIVIENDA)
# ==============================================================================

CASO_REGRESION = {
    "titulo": "Predicción Continua: Estimación de Precios Inmobiliarios",
    "descripcion": (
        "Un problema clásico de regresión supervisada donde el objetivo es predecir el valor comercial "
        "de un inmueble en función de características físicas y de ubicación."
    ),
    "formula": "Precio = β₀ + β₁(Metros Cuadrados) + β₂(Habitaciones) + β₃(Baños) + β₄(Antigüedad en Años) + ε",
    "dataset_ejemplo": [
        {"metros": 65, "habitaciones": 2, "banos": 1, "antiguedad": 12, "zona": "Centro", "precio_real": "$1,250,000 MXN", "predicho": "$1,242,000 MXN"},
        {"metros": 90, "habitaciones": 3, "banos": 2, "antiguedad": 8, "zona": "Residencial", "precio_real": "$1,890,000 MXN", "predicho": "$1,905,000 MXN"},
        {"metros": 130, "habitaciones": 4, "banos": 3, "antiguedad": 4, "zona": "Residencial", "precio_real": "$2,750,000 MXN", "predicho": "$2,710,000 MXN"},
        {"metros": 45, "habitaciones": 1, "banos": 1, "antiguedad": 20, "zona": "Periferia", "precio_real": "$780,000 MXN", "predicho": "$795,000 MXN"},
        {"metros": 180, "habitaciones": 4, "banos": 4, "antiguedad": 1, "zona": "Exclusiva", "precio_real": "$4,200,000 MXN", "predicho": "$4,180,000 MXN"}
    ],
    "metricas": [
        {"nombre": "R² Score (Coeficiente de Determinación)", "valor": "0.94", "interpretacion": "El modelo explica el 94% de la varianza en los precios de los inmuebles."},
        {"nombre": "MAE (Error Absoluto Medio)", "valor": "± $28,500 MXN", "interpretacion": "En promedio, la predicción desvía menos de 30 mil pesos del valor real."},
        {"nombre": "RMSE (Raíz del Error Cuadrático Medio)", "valor": "± $34,200 MXN", "interpretacion": "Penaliza errores grandes; confirma una alta solidez sin desviaciones extremas."}
    ],
    "codigo_python": '''# Implementación canónica de Regresión con Scikit-Learn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. Cargar el dataset estructurado
data = pd.read_csv('inmuebles.csv')
X = data[['metros_m2', 'habitaciones', 'banos', 'antiguedad_anios']]
y = data['precio_venta']

# 2. Partición rigurosa de datos (Train / Test split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Instanciación y Ajuste (Entrenamiento) del Modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# 4. Inferencia y Evaluación sobre datos nunca antes vistos
predicciones = modelo.predict(X_test)
print(f"R² Score: {r2_score(y_test, predicciones):.4f}")
print(f"Pesos de coeficientes aprendidos: {modelo.coef_}")
'''
}

# ==============================================================================
# 4. FUNCIÓN INTEGRADORA DEL MÓDULO
# ==============================================================================

def obtener_info_ml() -> Dict[str, Any]:
    """
    Retorna toda la información estructurada de Machine Learning,
    incluyendo teoría, ejemplos, dataset del modelo y métricas.
    """
    return {
        "teoria": INFO_MACHINE_LEARNING,
        "caso_regresion": CASO_REGRESION,
        "ejemplos_prueba": [
            {
                "tipo": "Spam / Phishing",
                "texto": "¡URGENTE! Has ganado 1,000,000 de pesos en la lotería nacional. Haz clic en este enlace para reclamar tu premio ya.",
                "icono": "fa-triangle-exclamation"
            },
            {
                "tipo": "Correo Académico Legítimo",
                "texto": "Hola profesor, le comparto el archivo con la tarea de Machine Learning correspondiente a la entrega final de IA.",
                "icono": "fa-graduation-cap"
            },
            {
                "tipo": "Alerta Falsa Bancaria (Phishing)",
                "texto": "Alerta de seguridad: Detectamos un acceso sospechoso. Ingrese su contraseña y número de tarjeta de inmediato para evitar el bloqueo.",
                "icono": "fa-credit-card"
            },
            {
                "tipo": "Coordinación de Estudio",
                "texto": "¿A qué hora nos vemos hoy en la biblioteca para repasar los temas del examen de redes neuronales?",
                "icono": "fa-users"
            }
        ]
    }
