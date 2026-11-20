# Portal Educativo de Inteligencia Artificial

Aplicación web educativa desarrollada con **Python + Flask** que reúne, en un solo portal, los principales temas de la asignatura de Inteligencia Artificial: glosario técnico, historia, clasificación, machine learning con un clasificador funcional, algoritmos de búsqueda con infografía interactiva y un ensayo académico sobre ética de la IA.

Incluye además una **demo independiente de DFS** (búsqueda en profundidad) con simulación visual animada sobre el plano de una casa.

---

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Apartados del portal](#apartados-del-portal)
- [API endpoints](#api-endpoints)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Despliegue en Vercel](#despliegue-en-vercel)
- [Notas de seguridad](#notas-de-seguridad)
- [Autor](#autor)

---

## Descripción general

El portal se sirve desde un único archivo `index.html` renderizado por Flask (`app.py`). La barra de navegación permite cambiar entre secciones sin recargar la página, y cada sección obtiene sus datos de un módulo Python independiente, lo que mantiene el contenido separado de la presentación.

Al iniciar el servidor se abre automáticamente el navegador en `http://127.0.0.1:5000/`.

---

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python 3, Flask 3.0.0 |
| Frontend | HTML5, CSS3 personalizado, JavaScript vanilla, SVG |
| UI | Bootstrap 5.3 (CDN), Font Awesome 6.4, Google Fonts (Inter, JetBrains Mono) |
| Machine Learning | Clasificador Naive Bayes implementado en Python puro (sin librerías externas) + integración con la API de Machine Learning for Kids |
| Demo DFS | Servidor HTTP estándar de Python (`http.server`), sin dependencias externas |
| Despliegue | Vercel (`@vercel/python`) |

Dependencias: ver [requirements.txt](requirements.txt) (solo Flask; el resto son comentarios de ejemplo).

---

## Estructura del proyecto

```
Web_py/
├── app.py                  # Servidor Flask: rutas, APIs y carga de todos los módulos
├── index.html              # Interfaz principal del portal (todas las secciones)
├── glosario.py             # Módulo 1: glosario de términos de IA
├── linea_tiempo.py         # Módulo 2: línea de tiempo histórica de la IA
├── clasificacion.py        # Módulo 3: clasificación de la IA (Débil / Fuerte / ASI + Hintze)
├── machine_learning.py     # Módulo 4: teoría de ML + clasificador Naive Bayes de spam
├── ensayo.py               # Módulo 5: ensayo académico de ética de la IA
├── algoritmo.py            # Módulo 6: algoritmos de búsqueda + infografía interactiva
├── DFS.py                  # Demo standalone: simulador visual DFS "Las llaves perdidas"
├── requirements.txt        # Dependencias (Flask==3.0.0)
├── vercel.json             # Configuración de despliegue en Vercel
└── static/
    ├── Ensayo_Etica_IA.pdf # PDF del ensayo (vista imprimible)
    └── logo_utp.jpg        # Logo institucional (Universidad Tecnológica de Puebla)
```

---

## Apartados del portal

### 1. Glosario de IA (`glosario.py`)

- **21 conceptos técnicos** de inteligencia artificial, desde los fundamentos (IA, Machine Learning, Deep Learning, NLP, Computer Vision) hasta temas de frontera (LLM, AGI, RAG, agentes autónomos, alucinaciones, prompt engineering).
- Organizados en **4 niveles de frecuencia de uso**: Muy Común, Poco Común, En Prueba y Apenas Apareciendo.
- Más de **20 categorías** (fundamentos, redes neuronales, paradigmas, ética y datos, síntesis creativa, etc.).
- Cada término incluye definición formal, imagen ilustrativa y una aplicación real.
- **Buscador con filtros**: por texto libre (`?q=`) y por nivel (`?nivel=`), con contador de resultados y estadísticas del glosario.

### 2. Línea de tiempo (`linea_tiempo.py`)

- **10 hitos históricos** de la IA, desde 1950 hasta la actualidad:
  - 1950-1956: nacimiento de la IA (Test de Turing, Conferencia de Dartmouth)
  - 1966: ELIZA, el primer chatbot
  - 1974-1980: el primer "invierno de la IA"
  - 1980-1987: sistemas expertos y backpropagation
  - 1997: Deep Blue vence a Kasparov
  - 2000-2009: despegue del machine learning estadístico
  - 2012-2016: revolución del deep learning y AlphaGo
  - 2020-2022: GPT y la explosión de la IA generativa
  - 2023-2024: multimodalidad y código abierto
  - 2025-presente: era de los agentes autónomos
- Cada hito incluye fechas detalladas, descripción, imagen y una **curiosidad histórica**.

### 3. Clasificación de la IA (`clasificacion.py`)

- **Clasificación por capacidad**:
  - **IA Débil (Narrow AI)**: la dominante hoy (Siri, Alexa, filtros de spam, recomendaciones).
  - **IA Fuerte (AGI)**: sistema teórico con cognición humana general.
  - **Superinteligencia (ASI)**: capacidad que superaría a la inteligencia humana en todos los dominios.
- Cada tipo incluye definición, características, límites e imágenes.
- **Taxonomía funcional de Arend Hintze** (4 niveles): máquinas reactivas, memoria limitada, teoría de la mente y autoconsciencia.

### 4. Machine Learning (`machine_learning.py`)

- **Base teórica completa**: definición formal de Tom Mitchell (1997), los **3 paradigmas** (supervisado, no supervisado y por refuerzo) con tipos, algoritmos y ejemplos, y el pipeline/ciclo de vida de un modelo de ML.
- **Clasificador de Spam/Phishing funcional**: implementación de **Naive Bayes en Python puro** (sin scikit-learn) entrenado con un dataset de 24 mensajes; expone probabilidades por clase y nivel de confianza.
- **Caso de regresión lineal múltiple**: ejemplo de predicción de precios de casas con dataset, métricas y código Python comentado.
- **4 ejemplos de prueba predefinidos** (spam, phishing bancario, correos legítimos) para probar el clasificador desde la interfaz.
- El portal integra además un **clasificador en vivo con Machine Learning for Kids** (ver endpoints abajo).

### 5. Ensayo académico (`ensayo.py`)

- Ensayo completo: *"Ética y Aspectos Sociales de la Inteligencia Artificial: Luces, Sombras y la Responsabilidad Humana en la Era Algorítmica"*.
- **6 secciones**: introducción + 5 ejes temáticos (sesgos algorítmicos y discriminación, automatización laboral y desigualdad, privacidad y capitalismo de vigilancia, autonomía y la "caja negra", gobernanza global antropocéntrica).
- Incluye resumen ejecutivo, palabras clave, citas destacadas y **7 referencias bibliográficas**.
- Se muestra incrustado el PDF generado ([static/Ensayo_Etica_IA.pdf](static/Ensayo_Etica_IA.pdf)) y existe una ruta de impresión (`/ensayo/imprimir`).

### 6. Algoritmos de búsqueda (`algoritmo.py`)

Investigación completa sobre algoritmos de búsqueda en IA:

- **Definición** y diferencia entre búsqueda en estructuras de datos e IA (espacio de estados).
- **Criterios de evaluación**: completitud, optimalidad, complejidad temporal y espacial.
- **Elementos** de un algoritmo de búsqueda y **ejemplo paso a paso** (BFS en un laberinto).
- **Clasificación** por múltiples criterios: ciega (BFS, DFS, UCS, IDDFS), heurística (greedy, A*, SMA*), local, adversarial y CSP.
- **Fichas detalladas** de algoritmos, **guía de selección** según el problema, **tabla comparativa** con leyenda, breve **historia** y **aplicaciones reales**.
- **Infografía interactiva** con taxonomía visual, dimensiones y fuentes.

### 7. Demo DFS: "Las llaves perdidas en la casa" (`DFS.py`)

Aplicación web **independiente y full-stack** (no requiere Flask ni ninguna dependencia externa):

- Backend en Python puro con `http.server` que construye el grafo bidireccional de una casa (14 lugares: sala, cocina, recámara, cochera...) con puertas bloqueables.
- Ejecuta **DFS** generando el recorrido paso a paso (ida y vuelta) y calcula la **distancia mínima real con BFS** para comparar resultados.
- Frontend en HTML5/SVG: plano arquitectónico con muros, ventanas y muebles ilustrados, detective animado con linterna, modo noche, sonido sintetizado y controles para bloquear puertas.
- API JSON en `POST /simular`; ejecución: `python DFS.py` y abrir `http://localhost:8000`.

---

## API endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Portal completo; admite `?sec=` (sección activa), `?q=` y `?nivel=` (filtros del glosario) |
| GET/POST | `/api/ml/predict` | Clasifica un texto como spam/no spam con el modelo Naive Bayes local (`texto` como parámetro o JSON) |
| POST | `/api/clasificador-ml4k/classify` | Clasifica texto con el modelo entrenado en Machine Learning for Kids (API key por cabecera `X-API-Key`, parámetro `api_key` o valor por defecto del portal) |
| GET | `/api/clasificador-ml4k/status` | Devuelve el estado de entrenamiento del modelo de ML for Kids |
| GET | `/ensayo/imprimir` | Vista de impresión A4 del ensayo (portada, índice, secciones y referencias) |

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
 git clone <url-del-repositorio>
 cd Web_py

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar el portal principal
python app.py
# Se abre automáticamente en http://127.0.0.1:5000/

# Demo independiente de DFS (puerto 8000)
python DFS.py
```

Requisito: Python 3.10+ (desarrollado con Python 3.14).

---

## Despliegue en Vercel

El archivo [vercel.json](vercel.json) configura el build con `@vercel/python` y redirige todas las rutas a `app.py`:

```bash
vercel --prod
```

---

## Notas de seguridad

- El clasificador de ML for Kids usa una API key configurable desde la interfaz; para producción se recomienda moverla a una **variable de entorno** en lugar de tenerla en el código fuente.
- No expongas claves reales en commits públicos; usa `.env` (añádelo a `.gitignore`) o variables de entorno del proveedor de hosting.

---

## Autor

**Cesar Hessiel Arevalo Sanchez**
Universidad Tecnológica de Puebla (UTP)
Área: Inteligencia Artificial y Sistemas Computacionales
Contacto: utp0153205@alumno.utpuebla.edu.mx
