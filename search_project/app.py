"""
Interfaz Web para el Motor de Búsqueda
========================================
Flask + HTML/CSS/JS moderno, responsive, sin dependencias externas CDN.
"""

from flask import Flask, render_template_string, request, jsonify
import sys
from pathlib import Path

# Añadir el directorio del motor al path
sys.path.insert(0, str(Path(__file__).parent))

from search_engine import SearchEngine, SAMPLE_DOCS

app = Flask(__name__)

# Motor global (se inicializa una vez)
engine = SearchEngine("hybrid")
engine.add_documents(SAMPLE_DOCS)


# =============================================================================
# PLANTILLA HTML (Single-file, sin dependencias externas)
# =============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor de Búsqueda</title>
    <style>
        /* ===== RESET & VARIABLES ===== */
        *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
        :root{
            --bg:#0a0f14;--bg-elev:#111820;--border:#1e2934;
            --fg:#e8ecf0;--fg-muted:#6b7a8c;--accent:#3b82f6;
            --accent-hover:#60a5fa;--success:#22c55e;--warn:#f59e0b;
            --danger:#ef4444;--card:#151d28;--input-bg:#0a0f14;
            --shadow:0 12px 32px rgba(0,0,0,.35);--radius:12px;
            --mono:'JetBrains Mono','Fira Code',ui-monospace,monospace;
            --sans:'Inter',system-ui,-apple-system,sans-serif;
        }
        @media (prefers-color-scheme: light){
            :root{--bg:#fafafa;--bg-elev:#ffffff;--border:#e5e7eb;
                --fg:#111827;--fg-muted:#6b7280;--accent:#2563eb;
                --accent-hover:#1d4ed8;--success:#16a34a;--warn:#d97706;
                --danger:#dc2626;--card:#ffffff;--input-bg:#f9fafb;
                --shadow:0 12px 32px rgba(0,0,0,.08);}
        }

        /* ===== BASE ===== */
        body{font-family:var(--sans);background:var(--bg);color:var(--fg);
            min-height:100vh;line-height:1.6;display:flex;flex-direction:column;
            -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;}
        .container{max-width:880px;width:100%;margin:0 auto;padding:clamp(1.5rem,4vw,3rem);}
        a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}

        /* ===== HEADER ===== */
        header{text-align:center;margin-bottom:2.5rem;}
        h1{font-size:clamp(2rem,5vw,3rem);font-weight:700;letter-spacing:-.03em;
            color:var(--fg);margin-bottom:.75rem;}
        .subtitle{color:var(--fg-muted);font-size:clamp(1rem,2vw,1.125rem);font-weight:400;}

        /* ===== SEARCH BOX ===== */
        .search-form{display:flex;gap:.75rem;margin-bottom:2rem;flex-wrap:wrap;}
        .search-input-wrapper{flex:1;min-width:300px;position:relative;}
        .search-input{width:100%;padding:1rem 1rem 1rem 3rem;
            font-size:1rem;font-family:var(--sans);background:var(--input-bg);
            border:1px solid var(--border);border-radius:var(--radius);color:var(--fg);
            transition:border-color .15s,box-shadow .15s,background-color .15s;}
        .search-input:focus{outline:none;border-color:var(--accent);
            box-shadow:0 0 0 3px rgba(59,130,246,.15);background:var(--bg-elev);}
        .search-input::placeholder{color:var(--fg-muted);}
        .search-icon{position:absolute;left:1rem;top:50%;transform:translateY(-50%);
            color:var(--fg-muted);pointer-events:none;width:20px;height:20px;}
        .btn{padding:1rem 1.75rem;font-size:.95rem;font-weight:500;font-family:var(--sans);
            border:none;border-radius:var(--radius);cursor:pointer;transition:all .15s;
            display:inline-flex;align-items:center;gap:.5rem;white-space:nowrap;}
        .btn-primary{background:var(--accent);color:#fff;}
        .btn-primary:hover{background:var(--accent-hover);transform:translateY(-1px);
            box-shadow:0 4px 16px rgba(59,130,246,.3);}
        .btn-primary:active{transform:translateY(0);}

        /* ===== CONTROLS ===== */
        .controls{display:flex;gap:1rem;flex-wrap:wrap;align-items:center;margin-bottom:1.5rem;
            padding:1rem 1.25rem;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);}
        .control-group{display:flex;align-items:center;gap:.5rem;}
        .control-label{font-size:.85rem;color:var(--fg-muted);white-space:nowrap;font-weight:500;}
        select,input[type="number"]{padding:.5rem .875rem;font-size:.85rem;font-family:var(--sans);
            background:var(--input-bg);border:1px solid var(--border);border-radius:8px;color:var(--fg);
            min-width:140px;}
        select:focus,input[type="number"]:focus{outline:none;border-color:var(--accent);}
        select{appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%236b7a8c' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right .75rem center;padding-right:2.5rem;}
        @media (prefers-color-scheme: light){
            select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");}
        }

        /* ===== STATS BAR ===== */
        .stats-bar{display:flex;gap:2rem;flex-wrap:wrap;margin-bottom:1.5rem;font-size:.85rem;color:var(--fg-muted);}
        .stat{display:flex;align-items:center;gap:.4rem;padding:.25rem .5rem;background:var(--card);border:1px solid var(--border);border-radius:8px;}
        .stat-value{font-weight:600;color:var(--fg);font-family:var(--mono);font-size:.85rem;}
        .stat-label{font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;}

        /* ===== RESULTS ===== */
        .results{display:flex;flex-direction:column;gap:1rem;}
        .result-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
            padding:1.5rem;transition:border-color .2s,box-shadow .2s,transform .15s;opacity:0;animation:fadeIn .4s ease forwards;}
        .result-card:hover{border-color:var(--accent);box-shadow:var(--shadow);transform:translateY(-2px);}
        @keyframes fadeIn{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}
        .result-header{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;margin-bottom:.75rem;flex-wrap:wrap;}
        .result-title{font-size:1.15rem;font-weight:600;color:var(--fg);line-height:1.35;}
        .result-score{background:rgba(59,130,246,.12);color:var(--accent);
            padding:.3rem .8rem;border-radius:999px;font-size:.75rem;font-weight:600;font-family:var(--mono);
            white-space:nowrap;flex-shrink:0;}
        .result-meta{display:flex;gap:1.5rem;flex-wrap:wrap;margin-bottom:1rem;font-size:.8rem;color:var(--fg-muted);}
        .result-meta span{display:flex;align-items:center;gap:.35rem;}
        .result-snippet{font-family:var(--mono);font-size:.875rem;line-height:1.7;color:var(--fg-muted);
            background:var(--bg);padding:1rem;border-radius:8px;border:1px solid var(--border);
            overflow-x:auto;white-space:pre-wrap;word-break:break-word;}
        .matched-terms{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1rem;}
        .term-tag{background:rgba(34,197,94,.12);color:var(--success);padding:.25rem .6rem;
            border-radius:6px;font-size:.7rem;font-weight:600;font-family:var(--mono);
            border:1px solid rgba(34,197,94,.2);}

        /* ===== EMPTY / LOADING ===== */
        .empty-state{text-align:center;padding:4rem 2rem;color:var(--fg-muted);}
        .empty-icon{width:64px;height:64px;margin:0 auto 1.5rem;opacity:.4;stroke:var(--fg-muted);}
        .empty-state p{font-size:1rem;max-width:400px;margin:0 auto .75rem;}
        .empty-state code{background:var(--card);border:1px solid var(--border);padding:.25rem .5rem;border-radius:4px;font-family:var(--mono);font-size:.85rem;}
        .loading{display:flex;flex-direction:column;align-items:center;gap:1rem;padding:3rem;color:var(--fg-muted);}
        .spinner{width:44px;height:44px;border:3px solid var(--border);border-top-color:var(--accent);
            border-radius:50%;animation:spin 1s linear infinite;}
        @keyframes spin{to{transform:rotate(360deg);}}

        /* ===== FOOTER ===== */
        footer{margin-top:auto;padding:2.5rem 0;text-align:center;color:var(--fg-muted);
            font-size:.85rem;border-top:1px solid var(--border);}
        footer a{color:var(--accent);}

        /* ===== RESPONSIVE ===== */
        @media (max-width:640px){
            .search-form{flex-direction:column;}
            .btn{width:100%;justify-content:center;}
            .controls{flex-direction:column;align-items:stretch;}
            .control-group{width:100%;justify-content:space-between;}
            .control-group select,.control-group input{flex:1;}
            .result-header{flex-direction:column;align-items:flex-start;}
            .stats-bar{gap:1rem;}
            .stat{flex:1;justify-content:center;}
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Motor de Búsqueda</h1>
            <p class="subtitle">Algoritmos: Híbrido · TF-IDF · Booleana · Difusa · DFS</p>
        </header>

        <form class="search-form" id="searchForm">
            <div class="search-input-wrapper">
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <input type="search" class="search-input" id="queryInput" placeholder="Buscar: python, machine learning, SQL, git..." autocomplete="off" required aria-label="Consulta de búsqueda">
            </div>
            <button type="submit" class="btn btn-primary" id="searchBtn" aria-label="Buscar">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                Buscar
            </button>
        </form>

        <div class="controls" role="group" aria-label="Controles de búsqueda">
            <div class="control-group">
                <label class="control-label" for="algoSelect">Algoritmo</label>
                <select id="algoSelect">
                    <option value="hybrid" selected>Híbrido (recomendado)</option>
                    <option value="tfidf">TF-IDF (ranking estadístico)</option>
                    <option value="boolean">Booleana (AND/OR/NOT)</option>
                    <option value="fuzzy">Difusa (Levenshtein)</option>
                    <option value="dfs">DFS (búsqueda en profundidad)</option>
                </select>
            </div>
            <div class="control-group">
                <label class="control-label" for="topKInput">Resultados</label>
                <input type="number" id="topKInput" min="1" max="50" value="10" aria-label="Número de resultados">
            </div>
            <div class="control-group" style="margin-left:auto;">
                <label class="control-label">
                    <input type="checkbox" id="highlightCheck" checked> Resaltar coincidencias
                </label>
            </div>
        </div>

        <div class="stats-bar" id="statsBar" style="display:none;" aria-live="polite">
            <div class="stat"><span class="stat-value" id="statDocs">0</span><span class="stat-label">documentos</span></div>
            <div class="stat"><span class="stat-value" id="statTokens">0</span><span class="stat-label">tokens</span></div>
            <div class="stat"><span class="stat-value" id="statTime">0</span><span class="stat-label">ms</span></div>
            <div class="stat"><span class="stat-value" id="statAlgo">-</span><span class="stat-label">algoritmo</span></div>
        </div>

        <div class="results" id="resultsContainer" aria-label="Resultados de búsqueda"></div>

        <div class="empty-state" id="emptyState" aria-live="polite">
            <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <p>Escribe una consulta para buscar en la base de conocimiento</p>
            <p style="font-size:.875rem;margin-top:.5rem;">Prueba: <code>python programación</code> · <code>búsqueda binaria</code> · <code>SQL optimización</code> · <code>git merge</code></p>
        </div>

        <div class="loading" id="loadingState" style="display:none;" aria-live="assertive">
            <div class="spinner" aria-hidden="true"></div>
            <span>Buscando...</span>
        </div>
    </div>

    <footer>
        Motor de búsqueda educativo · Algoritmos: Boolean, TF-IDF, Fuzzy, Hybrid, DFS
        <br><a href="https://github.com" target="_blank" rel="noopener">Ver código fuente</a>
    </footer>

    <script>
        // ===== ESTADO =====
        const $ = (sel) => document.querySelector(sel);
        const $$ = (sel) => document.querySelectorAll(sel);
        let lastQuery = '';

        // ===== ELEMENTOS =====
        const form = $('#searchForm');
        const input = $('#queryInput');
        const btn = $('#searchBtn');
        const algoSelect = $('#algoSelect');
        const topKInput = $('#topKInput');
        const highlightCheck = $('#highlightCheck');
        const resultsContainer = $('#resultsContainer');
        const emptyState = $('#emptyState');
        const loadingState = $('#loadingState');
        const statsBar = $('#statsBar');
        const statDocs = $('#statDocs');
        const statTokens = $('#statTokens');
        const statTime = $('#statTime');
        const statAlgo = $('#statAlgo');

        // ===== UTILIDADES =====
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function highlightTerms(text, terms) {
            if (!terms.length) return escapeHtml(text);
            const escaped = escapeHtml(text);
            const regex = new RegExp('(' + terms.map(t => t.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')).join('|') + ')', 'gi');
            return escaped.replace(regex, '<mark style="background:rgba(59,130,246,.25);color:var(--accent);padding:0 2px;border-radius:2px;">$1</mark>');
        }

        function makeSnippet(content, terms, maxLen = 300) {
            const lower = content.toLowerCase();
            let bestIdx = -1;
            for (const term of terms) {
                const idx = lower.indexOf(term.toLowerCase());
                if (idx !== -1) { bestIdx = idx; break; }
            }
            if (bestIdx === -1) return highlightTerms(content.slice(0, maxLen), terms) + '…';
            const start = Math.max(0, bestIdx - 100);
            const end = Math.min(content.length, bestIdx + maxLen);
            let snippet = content.slice(start, end);
            if (start > 0) snippet = '…' + snippet;
            if (end < content.length) snippet = snippet + '…';
            return highlightTerms(snippet, terms);
        }

        function formatTime(ms) {
            return ms < 1 ? '<1' : Math.round(ms);
        }

        // ===== RENDER =====
        function renderResults(results, query, elapsed, stats) {
            loadingState.style.display = 'none';
            statsBar.style.display = 'flex';

            statDocs.textContent = stats.documents.toLocaleString();
            statTokens.textContent = stats.total_tokens.toLocaleString();
            statTime.textContent = formatTime(elapsed);
            statAlgo.textContent = stats.algorithm_key;

            if (!results.length) {
                emptyState.style.display = 'block';
                resultsContainer.innerHTML = '';
                return;
            }

            emptyState.style.display = 'none';
            resultsContainer.innerHTML = results.map((r, i) => `
                <article class="result-card" style="animation-delay:${i * 50}ms">
                    <div class="result-header">
                        <h3 class="result-title">${escapeHtml(r.document.title)}</h3>
                        <span class="result-score">${(r.score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="result-meta">
                        <span>${escapeHtml(r.document.metadata.category || 'general')}</span>
                        <span>${escapeHtml(r.document.id)}</span>
                    </div>
                    <div class="result-snippet">${makeSnippet(r.snippet || r.document.content, r.matched_terms)}</div>
                    ${r.matched_terms.length ? `
                        <div class="matched-terms">
                            ${r.matched_terms.map(t => `<span class="term-tag">${escapeHtml(t)}</span>`).join('')}
                        </div>
                    ` : ''}
                </article>
            `).join('');
        }

        // ===== BÚSQUEDA =====
        async function doSearch(query) {
            if (!query.trim()) return;

            lastQuery = query;
            btn.disabled = true;
            btn.innerHTML = `<div class="spinner" style="width:18px;height:18px;border-width:2px;"></div> Buscando…`;
            loadingState.style.display = 'flex';
            emptyState.style.display = 'none';
            statsBar.style.display = 'none';

            try {
                const params = new URLSearchParams({
                    q: query,
                    algo: algoSelect.value,
                    top_k: topKInput.value,
                    highlight: highlightCheck.checked
                });
                const resp = await fetch(`/api/search?${params}`);
                const data = await resp.json();

                if (data.success) {
                    renderResults(data.results, query, data.elapsed_ms, data.stats);
                } else {
                    throw new Error(data.error || 'Error en búsqueda');
                }
            } catch (err) {
                console.error(err);
                resultsContainer.innerHTML = `
                    <article class="result-card" style="border-color:var(--danger);">
                        <div class="result-header">
                            <h3 class="result-title" style="color:var(--danger);">Error en la búsqueda</h3>
                        </div>
                        <div class="result-snippet">${escapeHtml(err.message)}</div>
                    </article>
                `;
                loadingState.style.display = 'none';
            } finally {
                btn.disabled = false;
                btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg> Buscar`;
            }
        }

        // ===== EVENTOS =====
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            doSearch(input.value.trim());
        });

        // Búsqueda al cambiar algoritmo o top-k
        [algoSelect, topKInput].forEach(el => {
            el.addEventListener('change', () => {
                if (lastQuery) doSearch(lastQuery);
            });
        });

        // Enter en input numérico
        topKInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && lastQuery) doSearch(lastQuery);
        });

        // Sugerencias rápidas (click en ejemplos)
        document.querySelectorAll('footer code').forEach(code => {
            code.style.cursor = 'pointer';
            code.addEventListener('click', () => {
                input.value = code.textContent;
                doSearch(code.textContent);
                input.focus();
            });
        });

        // Focus inicial
        input.focus();

        // Keyboard shortcut: / para enfocar
        document.addEventListener('keydown', (e) => {
            if (e.key === '/' && document.activeElement !== input) {
                e.preventDefault();
                input.focus();
            }
        });
    </script>
</body>
</html>
"""

# =============================================================================
# RUTAS
# =============================================================================

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/search")
def api_search():
    """Endpoint de búsqueda para AJAX."""
    from search_engine import SearchEngine

    query = request.args.get("q", "").strip()
    algo = request.args.get("algo", "hybrid")
    top_k = int(request.args.get("top_k", 10))

    if not query:
        return jsonify({"success": True, "results": [], "elapsed_ms": 0, "stats": engine.get_stats()})

    try:
        # Cambiar algoritmo si es necesario
        if engine.algorithm_name != algo:
            engine.set_algorithm(algo)

        results, elapsed = engine.search(query, top_k)
        return jsonify({
            "success": True,
            "results": [r.to_dict() for r in results],
            "elapsed_ms": elapsed,
            "stats": engine.get_stats()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats")
def api_stats():
    return jsonify(engine.get_stats())


@app.route("/api/algorithms")
def api_algorithms():
    return jsonify({
        "available": list(SearchEngine.ALGORITHMS.keys()),
        "current": engine.algorithm_name
    })


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Iniciando Motor de Busqueda Web")
    print("=" * 50)
    print(f"Documentos indexados: {len(engine.documents)}")
    print(f"Algoritmo actual: {engine.algorithm.name()}")
    print(f"Servidor: http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)