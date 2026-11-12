"""
Motor de Búsqueda Potente y Extensible
=======================================
Implementa múltiples algoritmos de búsqueda con una API unificada.
"""

from __future__ import annotations
import re
import time
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Optional
from collections import defaultdict, Counter
from pathlib import Path


# =============================================================================
# ESTRUCTURAS DE DATOS
# =============================================================================

@dataclass
class Document:
    """Representa un documento indexable."""
    id: str
    title: str
    content: str
    metadata: dict = field(default_factory=dict)
    _tokens: list[str] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        self._tokens = self._tokenize(self.content)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Tokenización simple: minúsculas, alfanumérico, stopwords básicas."""
        stopwords = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'uno', 'unos', 'unas', 'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas'}
        tokens = re.findall(r'\b\w+\b', text.lower())
        return [t for t in tokens if t not in stopwords and len(t) > 1]

    def get_tokens(self) -> list[str]:
        return self._tokens


@dataclass
class SearchResult:
    """Resultado de una búsqueda."""
    document: Document
    score: float
    matched_terms: list[str] = field(default_factory=list)
    snippet: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.document.id,
            "title": self.document.title,
            "snippet": self.snippet or self.document.content[:200] + "...",
            "score": round(self.score, 4),
            "matched_terms": self.matched_terms,
            "metadata": self.document.metadata
        }


# =============================================================================
# ALGORITMOS DE BÚSQUEDA (Strategy Pattern)
# =============================================================================

class SearchAlgorithm(ABC):
    """Interfaz base para algoritmos de búsqueda."""

    @abstractmethod
    def search(self, query: str, documents: list[Document], top_k: int = 10) -> list[SearchResult]:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class BooleanSearch(SearchAlgorithm):
    """Búsqueda booleana simple: AND/OR/NOT con tokens exactos."""

    def name(self) -> str:
        return "Booleana (AND/OR/NOT)"

    def search(self, query: str, documents: list[Document], top_k: int = 10) -> list[SearchResult]:
        # Parse simple: "term1 AND term2 OR term3 NOT term4"
        query = query.upper()
        and_terms = []
        or_terms = []
        not_terms = []

        # Extraer términos por operador
        parts = re.split(r'\s+(AND|OR|NOT)\s+', query)
        current_op = "AND"
        for part in parts:
            part = part.strip()
            if part in ("AND", "OR", "NOT"):
                current_op = part
            elif part:
                terms = part.lower().split()
                if current_op == "AND":
                    and_terms.extend(terms)
                elif current_op == "OR":
                    or_terms.extend(terms)
                elif current_op == "NOT":
                    not_terms.extend(terms)

        results = []
        for doc in documents:
            doc_tokens = set(doc.get_tokens())

            # Verificar NOT
            if any(nt in doc_tokens for nt in not_terms):
                continue

            # Verificar AND (todos deben estar)
            if and_terms and not all(at in doc_tokens for at in and_terms):
                continue

            # Verificar OR (al menos uno)
            if or_terms and not any(ot in doc_tokens for ot in or_terms):
                continue

            # Calcular score simple: coincidencias / total tokens query
            all_query_terms = and_terms + or_terms
            matched = [t for t in all_query_terms if t in doc_tokens]
            if not matched and not and_terms and not or_terms:
                continue

            score = len(matched) / max(len(all_query_terms), 1)
            snippet = self._make_snippet(doc.content, matched)

            results.append(SearchResult(
                document=doc,
                score=score,
                matched_terms=matched,
                snippet=snippet
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def _make_snippet(self, content: str, terms: list[str], window: int = 50) -> str:
        content_lower = content.lower()
        for term in terms:
            idx = content_lower.find(term)
            if idx != -1:
                start = max(0, idx - window)
                end = min(len(content), idx + len(term) + window)
                return "..." + content[start:end] + "..."
        return content[:150] + "..."


class TFIDFSearch(SearchAlgorithm):
    """Búsqueda TF-IDF (Term Frequency - Inverse Document Frequency).

    Potente para ranking por relevancia estadística.
    """

    def __init__(self):
        self._idf_cache: dict[str, float] = {}
        self._doc_freqs: dict[str, int] = {}
        self._total_docs: int = 0

    def name(self) -> str:
        return "TF-IDF (Ranking estadístico)"

    def _build_index(self, documents: list[Document]):
        """Construye índice invertido y calcula IDF."""
        self._total_docs = len(documents)
        self._doc_freqs = defaultdict(int)

        for doc in documents:
            unique_tokens = set(doc.get_tokens())
            for token in unique_tokens:
                self._doc_freqs[token] += 1

        # IDF = log(N / df)
        self._idf_cache = {
            token: math.log(self._total_docs / df)
            for token, df in self._doc_freqs.items()
        }

    def _tfidf_vector(self, tokens: list[str]) -> dict[str, float]:
        """Vector TF-IDF para un documento/consulta."""
        tf = Counter(tokens)
        max_tf = max(tf.values()) if tf else 1
        return {
            token: (count / max_tf) * self._idf_cache.get(token, 0)
            for token, count in tf.items()
        }

    def _cosine_similarity(self, vec1: dict[str, float], vec2: dict[str, float]) -> float:
        """Similitud coseno entre dos vectores TF-IDF."""
        if not vec1 or not vec2:
            return 0.0
        dot = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in set(vec1) & set(vec2))
        norm1 = math.sqrt(sum(v*v for v in vec1.values()))
        norm2 = math.sqrt(sum(v*v for v in vec2.values()))
        return dot / (norm1 * norm2) if norm1 and norm2 else 0.0

    def search(self, query: str, documents: list[Document], top_k: int = 10) -> list[SearchResult]:
        if not documents:
            return []

        self._build_index(documents)
        query_tokens = Document._tokenize(query)
        query_vec = self._tfidf_vector(query_tokens)

        results = []
        for doc in documents:
            doc_vec = self._tfidf_vector(doc.get_tokens())
            score = self._cosine_similarity(query_vec, doc_vec)

            if score > 0:
                matched = [t for t in query_tokens if t in doc.get_tokens()]
                snippet = self._make_snippet(doc.content, matched)
                results.append(SearchResult(
                    document=doc,
                    score=score,
                    matched_terms=matched,
                    snippet=snippet
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def _make_snippet(self, content: str, terms: list[str], window: int = 60) -> str:
        content_lower = content.lower()
        for term in terms:
            idx = content_lower.find(term)
            if idx != -1:
                start = max(0, idx - window)
                end = min(len(content), idx + len(term) + window)
                return "..." + content[start:end] + "..."
        return content[:180] + "..."


class FuzzySearch(SearchAlgorithm):
    """Búsqueda difusa (Levenshtein) - tolerante a errores tipográficos."""

    def name(self) -> str:
        return "Difusa (Levenshtein)"

    def _levenshtein(self, s1: str, s2: str, max_dist: int = 3) -> int:
        """Distancia de Levenshtein con early exit."""
        if abs(len(s1) - len(s2)) > max_dist:
            return max_dist + 1

        prev = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            curr = [i + 1]
            min_val = curr[0]
            for j, c2 in enumerate(s2):
                cost = 0 if c1 == c2 else 1
                curr.append(min(
                    prev[j + 1] + 1,      # deletion
                    curr[j] + 1,          # insertion
                    prev[j] + cost        # substitution
                ))
                min_val = min(min_val, curr[-1])
            if min_val > max_dist:
                return max_dist + 1
            prev = curr
        return prev[-1]

    def search(self, query: str, documents: list[Document], top_k: int = 10, max_dist: int = 2) -> list[SearchResult]:
        query_tokens = Document._tokenize(query)

        results = []
        for doc in documents:
            doc_tokens = doc.get_tokens()
            best_matches = []
            total_score = 0

            for qtoken in query_tokens:
                best_dist = max_dist + 1
                best_match = None
                for dtoken in doc_tokens:
                    dist = self._levenshtein(qtoken, dtoken, max_dist)
                    if dist < best_dist:
                        best_dist = dist
                        best_match = dtoken
                        if dist == 0:
                            break

                if best_dist <= max_dist:
                    # Score: 1.0 para exacto, decrece con distancia
                    score = 1.0 - (best_dist / (max_dist + 1))
                    total_score += score
                    best_matches.append((qtoken, best_match, best_dist))

            if best_matches:
                avg_score = total_score / len(query_tokens)
                matched_terms = [m[0] for m in best_matches]
                snippet = self._make_snippet(doc.content, matched_terms)
                results.append(SearchResult(
                    document=doc,
                    score=avg_score,
                    matched_terms=matched_terms,
                    snippet=snippet
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def _make_snippet(self, content: str, terms: list[str], window: int = 60) -> str:
        content_lower = content.lower()
        for term in terms:
            idx = content_lower.find(term)
            if idx != -1:
                start = max(0, idx - window)
                end = min(len(content), idx + len(term) + window)
                return "..." + content[start:end] + "..."
        return content[:180] + "..."


class HybridSearch(SearchAlgorithm):
    """Búsqueda híbrida: combina Boolean + TF-IDF + Fuzzy.

    La más potente: filtra con booleana, rankea con TF-IDF,
    expande con fuzzy si pocos resultados.
    """

    def __init__(self):
        self.boolean = BooleanSearch()
        self.tfidf = TFIDFSearch()
        self.fuzzy = FuzzySearch()

    def name(self) -> str:
        return "Hibrida (Booleana + TF-IDF + Fuzzy) [Recomendada]"

    def search(self, query: str, documents: list[Document], top_k: int = 10) -> list[SearchResult]:
        # 1. Intentar búsqueda booleana si hay operadores
        if any(op in query.upper() for op in (" AND ", " OR ", " NOT ")):
            results = self.boolean.search(query, documents, top_k * 2)
            if results:
                return results[:top_k]

        # 2. TF-IDF como búsqueda principal
        results = self.tfidf.search(query, documents, top_k)

        # 3. Si pocos resultados, expandir con fuzzy
        if len(results) < top_k:
            fuzzy_results = self.fuzzy.search(query, documents, top_k - len(results))
            # Merge evitando duplicados
            seen_ids = {r.document.id for r in results}
            for fr in fuzzy_results:
                if fr.document.id not in seen_ids:
                    results.append(fr)
                    seen_ids.add(fr.document.id)

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]


class DFSSearch(SearchAlgorithm):
    """Búsqueda por Profundidad (DFS) sobre grafo de documentos.

    Construye un grafo donde los nodos son documentos y las aristas
    representan similitud (términos compartidos, misma categoría).
    Inicia desde el documento más relevante y explora en profundidad.
    """

    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth
        self._graph: dict[str, list[str]] = {}
        self._doc_map: dict[str, Document] = {}

    def name(self) -> str:
        return "DFS (Búsqueda en profundidad)"

    def _build_graph(self, documents: list[Document]):
        """Construye grafo de similitud entre documentos."""
        self._doc_map = {doc.id: doc for doc in documents}
        self._graph = {doc.id: [] for doc in documents}

        # Conectar documentos que comparten categoría o términos
        for i, doc1 in enumerate(documents):
            for doc2 in documents[i + 1:]:
                shared = self._shared_terms(doc1, doc2)
                same_category = doc1.metadata.get("category") == doc2.metadata.get("category")
                if shared >= 2 or same_category:
                    self._graph[doc1.id].append(doc2.id)
                    self._graph[doc2.id].append(doc1.id)

    def _shared_terms(self, doc1: Document, doc2: Document) -> int:
        """Cuenta términos únicos compartidos entre dos documentos."""
        return len(set(doc1.get_tokens()) & set(doc2.get_tokens()))

    def _initial_scores(self, query: str, documents: list[Document]) -> list[tuple[str, float]]:
        """Calcula scores iniciales para encontrar nodo de partida."""
        query_tokens = set(Document._tokenize(query))
        scores = []
        for doc in documents:
            doc_tokens = set(doc.get_tokens())
            overlap = len(query_tokens & doc_tokens)
            if overlap > 0:
                score = overlap / len(query_tokens)
                scores.append((doc.id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def _dfs(self, start_id: str, visited: set[str], depth: int, results: list[SearchResult], query_tokens: set[str]):
        """Recorrido DFS recursivo."""
        if depth > self.max_depth or start_id in visited:
            return
        visited.add(start_id)

        doc = self._doc_map.get(start_id)
        if not doc:
            return

        doc_tokens = set(doc.get_tokens())
        matched = list(query_tokens & doc_tokens)
        if matched:
            score = len(matched) / len(query_tokens)
            # Penalizar por profundidad
            score *= (1.0 - depth * 0.15)
            snippet = self._make_snippet(doc.content, matched)
            results.append(SearchResult(
                document=doc,
                score=max(score, 0.05),
                matched_terms=matched,
                snippet=snippet
            ))

        # Explorar vecinos
        for neighbor_id in self._graph.get(start_id, []):
            self._dfs(neighbor_id, visited, depth + 1, results, query_tokens)

    def search(self, query: str, documents: list[Document], top_k: int = 10) -> list[SearchResult]:
        if not documents:
            return []

        self._build_graph(documents)
        query_tokens = set(Document._tokenize(query))

        # Encontrar mejor nodo inicial
        initial_scores = self._initial_scores(query, documents)
        if not initial_scores:
            return []

        # DFS desde los mejores nodos iniciales
        all_results = []
        visited_global = set()

        for start_id, start_score in initial_scores[:3]:  # Top 3 semillas
            if start_id in visited_global:
                continue
            results = []
            self._dfs(start_id, set(), 0, results, query_tokens)
            all_results.extend(results)
            visited_global.update(r.document.id for r in results)
            if len(all_results) >= top_k:
                break

        # Deduplicar y ordenar
        seen = set()
        unique_results = []
        for r in all_results:
            if r.document.id not in seen:
                seen.add(r.document.id)
                unique_results.append(r)

        unique_results.sort(key=lambda r: r.score, reverse=True)
        return unique_results[:top_k]

    def _make_snippet(self, content: str, terms: list[str], window: int = 60) -> str:
        content_lower = content.lower()
        for term in terms:
            idx = content_lower.find(term)
            if idx != -1:
                start = max(0, idx - window)
                end = min(len(content), idx + len(term) + window)
                return "..." + content[start:end] + "..."
        return content[:180] + "..."


# =============================================================================
# MOTOR DE BÚSQUEDA PRINCIPAL (Fachada)
# =============================================================================

class SearchEngine:
    """Motor de búsqueda unificado con múltiples algoritmos."""

    ALGORITHMS = {
        "boolean": BooleanSearch,
        "tfidf": TFIDFSearch,
        "fuzzy": FuzzySearch,
        "hybrid": HybridSearch,
        "dfs": DFSSearch,
    }

    def __init__(self, algorithm: str = "hybrid"):
        self.algorithm_name = algorithm
        self.algorithm = self.ALGORITHMS[algorithm]()
        self.documents: list[Document] = []
        self._indexed = False

    def add_document(self, doc: Document):
        self.documents.append(doc)
        self._indexed = False

    def add_documents(self, docs: list[Document]):
        self.documents.extend(docs)
        self._indexed = False

    def load_from_directory(self, path: str, pattern: str = "*.txt", encoding: str = "utf-8"):
        """Carga documentos desde archivos en un directorio."""
        p = Path(path)
        for file_path in p.glob(pattern):
            try:
                content = file_path.read_text(encoding=encoding)
                doc = Document(
                    id=file_path.stem,
                    title=file_path.name,
                    content=content,
                    metadata={"path": str(file_path), "size": len(content)}
                )
                self.add_document(doc)
            except Exception as e:
                print(f"Error leyendo {file_path}: {e}")

    def set_algorithm(self, algorithm: str):
        if algorithm in self.ALGORITHMS:
            self.algorithm_name = algorithm
            self.algorithm = self.ALGORITHMS[algorithm]()
            self._indexed = False
        else:
            raise ValueError(f"Algoritmo desconocido: {algorithm}. Disponibles: {list(self.ALGORITHMS.keys())}")

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        if not self.documents:
            return []
        start = time.perf_counter()
        results = self.algorithm.search(query, self.documents, top_k)
        elapsed = (time.perf_counter() - start) * 1000
        return results, elapsed

    def get_stats(self) -> dict:
        total_tokens = sum(len(d.get_tokens()) for d in self.documents)
        return {
            "algorithm": self.algorithm.name(),
            "algorithm_key": self.algorithm_name,
            "documents": len(self.documents),
            "total_tokens": total_tokens,
            "avg_tokens_per_doc": round(total_tokens / len(self.documents), 1) if self.documents else 0,
            "available_algorithms": list(self.ALGORITHMS.keys())
        }


# =============================================================================
# DATOS DE EJEMPLO
# =============================================================================

SAMPLE_DOCS = [
    Document(
        id="1",
        title="Introducción a Python",
        content="Python es un lenguaje de programación interpretado, de alto nivel y de propósito general. "
                "Su filosofía de diseño enfatiza la legibilidad del código con el uso de sangría significativa. "
                "Python soporta múltiples paradigmas: programación orientada a objetos, imperativa y funcional. "
                "Cuenta con una amplia biblioteca estándar y una gran comunidad de desarrolladores.",
        metadata={"category": "programación", "language": "es"}
    ),
    Document(
        id="2",
        title="Algoritmos de Búsqueda",
        content="Los algoritmos de búsqueda son fundamentales en ciencias de la computación. "
                "Búsqueda lineal: recorre elementos secuencialmente O(n). "
                "Búsqueda binaria: divide y vencerás en arrays ordenados O(log n). "
                "Búsqueda en profundidad (DFS) y anchura (BFS) para grafos y árboles. "
                "Algoritmo A* combina heurística y costo real para pathfinding óptimo.",
        metadata={"category": "algoritmos", "language": "es"}
    ),
    Document(
        id="3",
        title="Machine Learning Basics",
        content="Machine Learning es una rama de la inteligencia artificial que permite a las máquinas "
                "aprender de los datos sin ser programadas explícitamente. "
                "Tipos principales: aprendizaje supervisado (regresión, clasificación), "
                "no supervisado (clustering, reducción de dimensionalidad), "
                "y por refuerzo (agentes, recompensas). Algoritmos populares: "
                "Regresión lineal, Árboles de decisión, Random Forest, SVM, Redes neuronales.",
        metadata={"category": "IA", "language": "es"}
    ),
    Document(
        id="4",
        title="Estructuras de Datos en Python",
        content="Python incluye estructuras de datos potentes: listas (arrays dinámicos), "
                "tuplas (inmutables), diccionarios (hash tables O(1)), conjuntos (sets), "
                "y collections.deque (colas dobles). Para rendimiento: array.array, "
                "numpy.ndarray, pandas.DataFrame. Entender complejidad temporal "
                "es clave para elegir la estructura correcta.",
        metadata={"category": "programación", "language": "es"}
    ),
    Document(
        id="5",
        title="Bases de Datos y SQL",
        content="SQL (Structured Query Language) es el lenguaje estándar para bases de datos relacionales. "
                "Comandos principales: SELECT, INSERT, UPDATE, DELETE. "
                "Joins: INNER, LEFT, RIGHT, FULL. Índices B-Tree aceleran búsquedas. "
                "ACID: Atomicidad, Consistencia, Aislamiento, Durabilidad. "
                "NoSQL: MongoDB (documentos), Redis (clave-valor), Cassandra (columnas).",
        metadata={"category": "bases de datos", "language": "es"}
    ),
    Document(
        id="6",
        title="Redes Neuronales y Deep Learning",
        content="Las redes neuronales artificiales se inspiran en el cerebro humano. "
                "Perceptrón: unidad básica. Capas: entrada, ocultas, salida. "
                "Funciones de activación: ReLU, Sigmoid, Tanh, Softmax. "
                "Backpropagation y Gradient Descent para entrenamiento. "
                "Arquitecturas: CNN (imágenes), RNN/LSTM (secuencias), Transformers (NLP). "
                "Frameworks: TensorFlow, PyTorch, Keras, JAX.",
        metadata={"category": "IA", "language": "es"}
    ),
    Document(
        id="7",
        title="Optimización de Consultas SQL",
        content="Optimizar consultas SQL mejora rendimiento drásticamente. "
                "Usar EXPLAIN para ver plan de ejecución. "
                "Índices compuestos para WHERE y JOIN. Evitar SELECT *. "
                "Límites con LIMIT. Subconsultas vs JOINs. "
                "Particionamiento de tablas grandes. Caché de consultas frecuentes.",
        metadata={"category": "bases de datos", "language": "es"}
    ),
    Document(
        id="8",
        title="Git y Control de Versiones",
        content="Git es un sistema de control de versiones distribuido. "
                "Comandos esenciales: init, clone, add, commit, push, pull, branch, merge, rebase. "
                "Flujo GitFlow: main, develop, feature/*, release/*, hotfix/*. "
                "Resolución de conflictos. Git bisect para encontrar bugs. "
                "Hooks: pre-commit, pre-push. GitHub/GitLab/Bitbucket como remotos.",
        metadata={"category": "herramientas", "language": "es"}
    ),
]


# =============================================================================
# DEMO / TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 MOTOR DE BÚSQUEDA - DEMO")
    print("=" * 60)

    # Crear motor con algoritmo híbrido (recomendado)
    engine = SearchEngine("hybrid")
    engine.add_documents(SAMPLE_DOCS)

    stats = engine.get_stats()
    print(f"\n📊 Índice: {stats['documents']} docs, {stats['total_tokens']} tokens")
    print(f"🔧 Algoritmo: {stats['algorithm']}")

    # Consultas de prueba
    test_queries = [
        "python programación",
        "búsqueda binaria",
        "machine learning redes neuronales",
        "SQL optimización índices",
        "git merge rebase",
        "algoritmo A* pathfinding",
    ]

    for query in test_queries:
        print(f"\n🔎 Consulta: '{query}'")
        results, ms = engine.search(query, top_k=3)
        print(f"   ⏱️  {ms:.2f}ms - {len(results)} resultados")
        for i, r in enumerate(results, 1):
            print(f"   {i}. [{r.score:.3f}] {r.document.title}")
            print(f"      📝 {r.snippet[:100]}...")

    print("\n" + "=" * 60)
    print("✅ Demo completado. Importa SearchEngine en tu código.")
    print("=" * 60)