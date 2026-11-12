# 🔍 Motor de Búsqueda IA - Proyecto Completo

Un motor de búsqueda **potente, extensible y educativo** con interfaz web moderna.

## ✨ Características

| Algoritmo | Descripción | Caso de Uso |
|-----------|-------------|-------------|
| **Híbrido** ⭐ | Combina Booleana + TF-IDF + Difusa | **Recomendado por defecto** |
| **TF-IDF** | Ranking estadístico por relevancia | Búsqueda general, documentos largos |
| **Booleana** | AND / OR / NOT exactos | Consultas precisas, filtros |
| **Difusa (Levenshtein)** | Tolerante a errores tipográficos | Usuarios con typos, OCR, nombres |

## 🚀 Inicio Rápido

```bash
# 1. Entrar al directorio
cd D:/7C/IA/Algoritmo/search_project

# 2. Crear entorno virtual (recomendado)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python app.py
```

Abre **http://localhost:5000** en tu navegador.

## 📁 Estructura del Proyecto

```
search_project/
├── search_engine.py    # Motor principal (algoritmos + índice)
├── app.py              # Servidor Flask + UI web
├── requirements.txt    # Dependencias (solo Flask)
└── README.md           # Este archivo
```

## 💻 Uso Programático (sin web)

```python
from search_engine import SearchEngine, Document, SAMPLE_DOCS

# Crear motor
engine = SearchEngine("hybrid")  # o "tfidf", "boolean", "fuzzy"
engine.add_documents(SAMPLE_DOCS)

# Buscar
results, ms = engine.search("python programación", top_k=5)

for r in results:
    print(f"[{r.score:.3f}] {r.document.title}")
    print(f"  {r.snippet[:100]}...")
    print(f"  Términos: {r.matched_terms}")
```

## 🌐 API REST

| Endpoint | Método | Parámetros | Respuesta |
|----------|--------|------------|-----------|
| `/api/search` | GET | `q`, `algo`, `top_k` | `{success, results[], elapsed_ms, stats}` |
| `/api/stats` | GET | - | Estadísticas del índice |
| `/api/algorithms` | GET | - | Algoritmos disponibles |

**Ejemplo:**
```bash
curl "http://localhost:5000/api/search?q=machine+learning&algo=tfidf&top_k=3"
```

## 🔧 Extender el Motor

### Agregar tus propios documentos

```python
# Desde archivos
engine.load_from_directory("./mis_documentos", "*.txt")

# Programáticamente
engine.add_document(Document(
    id="mi-doc-1",
    title="Mi Documento",
    content="Contenido completo del documento...",
    metadata={"autor": "Yo", "fecha": "2024"}
))
```

### Crear algoritmo personalizado

```python
from search_engine import SearchAlgorithm, SearchResult, Document

class MiAlgoritmo(SearchAlgorithm):
    def name(self): return "Mi Algoritmo Personalizado"
    
    def search(self, query, documents, top_k=10):
        # Tu lógica aquí
        results = []
        for doc in documents:
            score = tu_funcion_de_scoring(query, doc)
            if score > 0:
                results.append(SearchResult(document=doc, score=score, ...))
        return sorted(results, key=lambda r: r.score, reverse=True)[:top_k]

# Registrar
SearchEngine.ALGORITHMS["mi_algo"] = MiAlgoritmo
engine = SearchEngine("mi_algo")
```

## 🎯 Consultas de Prueba

Prueba estas búsquedas en la web:

| Consulta | Algoritmo Recomendado | Qué Demuestra |
|----------|----------------------|---------------|
| `python programación` | Híbrida / TF-IDF | Búsqueda semántica básica |
| `búsqueda binaria` | Híbrida / TF-IDF | Términos técnicos |
| `machine learning redes neuronales` | TF-IDF | Múltiples términos relacionados |
| `SQL optimización índices` | Booleana / Híbrida | Dominio específico |
| `git merge rebase` | Híbrida | Siglas + verbos |
| `algoritmo A* pathfinding` | Difusa / Híbrida | Símbolos especiales (*) |
| `pyton programacion` | **Difusa** | **Typos intencionales** |
| `python AND programación NOT java` | **Booleana** | **Operadores lógicos** |

## 📚 Algoritmos Implementados - Detalle Técnico

### TF-IDF (Term Frequency × Inverse Document Frequency)
```
tf(t,d) = count(t,d) / max_tf(d)
idf(t) = log(N / df(t))
score(q,d) = cosine_similarity(tfidf(q), tfidf(d))
```

### Levenshtein (Distancia de Edición)
- Programación dinámica O(m×n)
- Early exit si distancia > `max_dist` (default 2)
- Score = 1 - dist/(max_dist+1)

### Híbrida (Pipeline)
1. **Booleana** si detecta operadores → filtra exacto
2. **TF-IDF** → ranking estadístico principal
3. **Difusa** si pocos resultados → expande recall

## 🎨 Personalizar UI

La interfaz está en `app.py` como `HTML_TEMPLATE` (string único).
- **CSS**: Variables en `:root` (tema oscuro/claro automático)
- **JS**: Vanilla ES6, sin dependencias
- **Responsive**: Mobile-first, breakpoints en 600px

## 📄 Licencia

MIT - Úsalo libremente para aprender, enseñar o producir.

---

**¿Dudas? ¿Mejoras?** El código está documentado y es modular. ¡Explora `search_engine.py`!