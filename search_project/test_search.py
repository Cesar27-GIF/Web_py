"""
Script de Prueba Rapida del Motor de Busqueda
==============================================
Ejecuta: python test_search.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from search_engine import SearchEngine, SAMPLE_DOCS


def test_all_algorithms():
    """Prueba todos los algoritmos con consultas variadas."""
    queries = [
        "python programacion",
        "busqueda binaria",
        "machine learning redes neuronales",
        "SQL optimizacion indices",
        "git merge rebase",
        "algoritmo A* pathfinding",
        "pyton programacion",  # typo para fuzzy
    ]

    algorithms = ["hybrid", "tfidf", "boolean", "fuzzy", "dfs"]

    for algo_name in algorithms:
        print(f"\n{'='*60}")
        print(f"ALGORITMO: {algo_name.upper()}")
        print(f"{'='*60}")

        engine = SearchEngine(algo_name)
        engine.add_documents(SAMPLE_DOCS)

        for query in queries:
            results, ms = engine.search(query, top_k=3)
            print(f"\nConsulta: '{query}' ({ms:.1f}ms) -> {len(results)} resultados")
            for i, r in enumerate(results, 1):
                print(f"   {i}. [{r.score:.3f}] {r.document.title}")
                if r.matched_terms:
                    print(f"      Coincidencias: {r.matched_terms}")


def test_boolean_operators():
    """Prueba operadores booleanos."""
    print(f"\n{'='*60}")
    print(f"PRUEBA OPERADORES BOOLEANOS")
    print(f"{'='*60}")

    engine = SearchEngine("boolean")
    engine.add_documents(SAMPLE_DOCS)

    boolean_queries = [
        "python AND programacion",
        "machine OR learning",
        "SQL NOT python",
        "busqueda AND binaria OR lineal",
    ]

    for query in boolean_queries:
        results, ms = engine.search(query, top_k=3)
        print(f"\nConsulta: '{query}' -> {len(results)} resultados")
        for i, r in enumerate(results, 1):
            print(f"   {i}. [{r.score:.3f}] {r.document.title}")


def test_fuzzy_typos():
    """Prueba tolerancia a errores tipograficos."""
    print(f"\n{'='*60}")
    print(f"PRUEBA BUSQUEDA DIFUSA (TYPO)")
    print(f"{'='*60}")

    engine = SearchEngine("fuzzy")
    engine.add_documents(SAMPLE_DOCS)

    typos = [
        ("python", "pyton"),
        ("machine", "mashine"),
        ("algoritmo", "algortimo"),
        ("busqueda", "busqueda"),
        ("redes neuronales", "redes neuronale"),
    ]

    for original, typo in typos:
        results, ms = engine.search(typo, top_k=2)
        print(f"\nConsulta: '{typo}' (original: '{original}') -> {len(results)} resultados")
        for r in results:
            print(f"   [{r.score:.3f}] {r.document.title} -- match: {r.matched_terms}")


def test_engine_stats():
    """Muestra estadisticas del motor."""
    print(f"\n{'='*60}")
    print(f"ESTADISTICAS DEL INDICE")
    print(f"{'='*60}")

    engine = SearchEngine("hybrid")
    engine.add_documents(SAMPLE_DOCS)
    stats = engine.get_stats()

    for k, v in stats.items():
        print(f"   {k}: {v}")


if __name__ == "__main__":
    print("TESTS DEL MOTOR DE BUSQUEDA")
    print("=" * 60)

    test_engine_stats()
    test_all_algorithms()
    test_boolean_operators()
    test_fuzzy_typos()

    print(f"\n{'='*60}")
    print("Todos los tests completados")
    print("=" * 60)