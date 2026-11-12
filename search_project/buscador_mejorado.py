"""Buscador visual: Python (backend) + HTML/SVG (frontend). Sin instalar nada.
Correr:  python buscador_mejorado.py   ->  abrir http://localhost:8000
Cada paso trae una explicación; al final se explica por qué se encontró o no.
"""
import json
import random
from collections import deque, defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer


# ---------- Información de cada algoritmo (complejidad + pseudocódigo) ----------
INFO = {
    "lineal": {
        "nombre": "Búsqueda lineal",
        "mejor": "O(1)", "promedio": "O(n)", "peor": "O(n)", "memoria": "O(1)",
        "nota": "No necesita la lista ordenada. Revisa elemento por elemento.",
        "pseudo": [
            "para i desde 0 hasta n-1:",
            "    si lista[i] == objetivo:",
            "        devolver i",
            "devolver \"no está\"",
        ],
    },
    "binaria": {
        "nombre": "Búsqueda binaria",
        "mejor": "O(1)", "promedio": "O(log n)", "peor": "O(log n)", "memoria": "O(1)",
        "nota": "Requiere lista ordenada (ordenarla cuesta O(n log n)). Descarta la mitad en cada paso.",
        "pseudo": [
            "lista = ordenar(lista)",
            "izq = 0 ; der = n-1",
            "mientras izq <= der:",
            "    mid = (izq + der) // 2",
            "    si lista[mid] == objetivo: devolver mid",
            "    si lista[mid] < objetivo: izq = mid + 1",
            "    si no: der = mid - 1",
            "devolver \"no está\"",
        ],
    },
    "profundidad": {
        "nombre": "Profundidad (DFS)",
        "mejor": "O(1)", "promedio": "O(V+E)", "peor": "O(V+E)", "memoria": "O(V)",
        "nota": "Usa una pila (LIFO). Baja lo más profundo posible; no garantiza el camino más corto.",
        "pseudo": [
            "pila = [inicio] ; visitados = {inicio}",
            "mientras la pila no esté vacía:",
            "    nodo = pila.sacar_tope()",
            "    si nodo == objetivo: devolver camino",
            "    para cada vecino no visitado de nodo:",
            "        marcar visitado ; pila.apilar(vecino)",
            "devolver \"no está\"",
        ],
    },
    "anchura": {
        "nombre": "Anchura (BFS)",
        "mejor": "O(1)", "promedio": "O(V+E)", "peor": "O(V+E)", "memoria": "O(V)",
        "nota": "Usa una cola (FIFO). Avanza por niveles; garantiza el camino más corto (sin pesos).",
        "pseudo": [
            "cola = [inicio] ; visitados = {inicio}",
            "mientras la cola no esté vacía:",
            "    nodo = cola.sacar_frente()",
            "    si nodo == objetivo: devolver camino",
            "    para cada vecino no visitado de nodo:",
            "        marcar visitado ; cola.encolar(vecino)",
            "devolver \"no está\"",
        ],
    },
}


# ---------- Algoritmos ----------
def _norm(v, tipo="auto"):
    """Compara '5' con '5.0' como numero; si tipo='texto' siempre como texto."""
    v = str(v).strip()
    if tipo == "texto":
        return (1, v.lower())
    try:
        return (0, float(v))
    except ValueError:
        return (1, v.lower())


def busqueda_lineal(lista, objetivo, tipo="auto"):
    """O(n): revisa uno por uno."""
    recorrido = []
    for i, v in enumerate(lista):
        ok = _norm(v, tipo) == _norm(objetivo, tipo)
        ultimo = i == len(lista) - 1
        if ok:
            texto = f"Posición {i}: {v} es igual a {objetivo}. ¡Coincide!"
            linea = 2
        elif ultimo:
            texto = f"Posición {i}: {v} no es {objetivo}. Era el último: se acabó la lista."
            linea = 3
        else:
            texto = f"Posición {i}: {v} no es {objetivo}. Paso al siguiente."
            linea = 1
        recorrido.append({"indice": i, "valor": v, "texto": texto, "linea": linea})
        if ok:
            return {
                "encontrado": True, "indice": i, "recorrido": recorrido,
                "resumen": f"Lo encontré en la posición {i}, después de revisar {i + 1} "
                           f"elemento(s) de izquierda a derecha.",
            }
    return {
        "encontrado": False, "indice": -1, "recorrido": recorrido,
        "resumen": f"Revisé los {len(lista)} elementos uno por uno y ninguno es igual a "
                   f"{objetivo}. Como la búsqueda lineal recorre toda la lista, puedo "
                   f"asegurar que no está. Si esperabas verlo, revisa cómo lo escribiste "
                   f"y que el tipo de dato elegido sea el correcto.",
    }


def busqueda_binaria(lista, objetivo, tipo="auto"):
    """O(log n): ordena y va partiendo el rango a la mitad."""
    ordenada = sorted(lista, key=lambda x: _norm(x, tipo))
    izq, der = 0, len(ordenada) - 1
    recorrido = []
    intro = "La binaria necesita una lista ordenada, así que primero la ordené."
    while izq <= der:
        mid = (izq + der) // 2
        v = ordenada[mid]
        base = f"Rango {izq}–{der}, miro el medio (posición {mid}): {v}. "
        if _norm(v, tipo) == _norm(objetivo, tipo):
            texto = base + "Es igual al objetivo. ¡Encontrado!"
            linea = 4
        elif _norm(v, tipo) < _norm(objetivo, tipo):
            texto = base + (f"Es menor que {objetivo}, así que si existe está a la derecha. "
                            f"Descarto las posiciones {izq}–{mid}.")
            linea = 5
        else:
            texto = base + (f"Es mayor que {objetivo}, así que si existe está a la izquierda. "
                            f"Descarto las posiciones {mid}–{der}.")
            linea = 6
        recorrido.append({"indice": mid, "valor": v, "rango": [izq, der],
                          "texto": texto, "linea": linea})
        if linea == 4:
            return {
                "encontrado": True, "indice": mid, "ordenada": ordenada, "recorrido": recorrido,
                "intro": intro,
                "resumen": f"Lo encontré en la posición {mid} de la lista ordenada con solo "
                           f"{len(recorrido)} comparación(es), en vez de revisar los "
                           f"{len(ordenada)} elementos.",
            }
        if linea == 5:
            izq = mid + 1
        else:
            der = mid - 1
    return {
        "encontrado": False, "indice": -1, "ordenada": ordenada, "recorrido": recorrido,
        "intro": intro,
        "resumen": f"El rango se fue achicando hasta quedar vacío: ya no quedan posiciones por "
                   f"mirar. En una lista ordenada eso demuestra que {objetivo} no está. "
                   f"Lo comprobé con {len(recorrido)} comparación(es).",
    }


def _por_que_no(grafo, inicio, objetivo):
    """Diagnostica por qué un nodo no fue alcanzado."""
    if objetivo not in grafo:
        parecido = next((n for n in grafo if n.lower() == objetivo.lower()), None)
        if parecido:
            return (f"{objetivo} no existe, pero sí {parecido}: los nombres de nodo "
                    f"distinguen mayúsculas de minúsculas.")
        return (f"{objetivo} no es ningún nodo del grafo. Revisa que esté escrito igual "
                f"que en las conexiones.")
    sin_dir = defaultdict(set)
    for a, vecinos in grafo.items():
        for b in vecinos:
            sin_dir[a].add(b)
            sin_dir[b].add(a)
    visto, pend = {inicio}, [inicio]
    while pend:
        n = pend.pop()
        for v in sin_dir[n]:
            if v not in visto:
                visto.add(v)
                pend.append(v)
    if objetivo in visto:
        return (f"{objetivo} sí está conectado al grafo, pero las flechas apuntan en sentido "
                f"contrario y no se puede llegar desde {inicio}. Prueba activar Sin "
                f"dirección o cambiar el nodo inicial.")
    return (f"{objetivo} está en el grafo, pero ninguna conexión lo une con {inicio}: "
            f"está en una parte aislada.")


def busqueda_profundidad(grafo, inicio, objetivo):
    """DFS: pila (LIFO), baja lo mas profundo posible antes de volver."""
    pila = [(inicio, [inicio])]
    visitados = {inicio}
    recorrido = []
    while pila:
        nodo, camino = pila.pop()
        arranque = f"Empiezo en {nodo}. " if not recorrido else ""
        if nodo == objetivo:
            recorrido.append({
                "nodo": nodo, "sacado": nodo, "linea": 3,
                "estructura": [n for n, _ in pila],
                "texto": f"{arranque}Saco {nodo} de la pila: es el objetivo. ¡Encontrado!"})
            return {
                "encontrado": True, "camino": camino, "recorrido": recorrido,
                "resumen": f"Llegué a {objetivo} por el camino {' → '.join(camino)} "
                           f"({len(camino) - 1} salto(s)). DFS baja lo más profundo que puede, "
                           f"así que este camino no siempre es el más corto.",
            }
        nuevos = [v for v in grafo.get(nodo, []) if v not in visitados]
        if nuevos:
            linea = 5
            texto = (f"{arranque}Saco {nodo} de la pila: no es {objetivo}. Apilo sus "
                     f"vecinos nuevos ({', '.join(nuevos)}) y sigo por {nuevos[0]}, "
                     f"bajando lo más profundo posible.")
        elif pila:
            linea = 4
            texto = (f"{arranque}Saco {nodo}: no es {objetivo} y no tiene vecinos nuevos. "
                     f"Es un callejón sin salida, retrocedo a {pila[-1][0]}, el último "
                     f"pendiente de la pila.")
        else:
            linea = 6
            texto = (f"{arranque}Saco {nodo}: no es {objetivo}, no tiene vecinos nuevos y "
                     f"la pila ya está vacía. No queda nada por explorar.")
        for v in reversed(nuevos):
            visitados.add(v)
            pila.append((v, camino + [v]))
        recorrido.append({"nodo": nodo, "sacado": nodo, "linea": linea,
                          "estructura": [n for n, _ in pila], "texto": texto})
    orden = ", ".join(p["nodo"] for p in recorrido)
    return {
        "encontrado": False, "camino": [], "recorrido": recorrido,
        "resumen": f"Exploré todo lo que se puede alcanzar desde {inicio} ({orden}) y la pila "
                   f"quedó vacía sin toparme con {objetivo}. "
                   + _por_que_no(grafo, inicio, objetivo),
    }


def busqueda_anchura(grafo, inicio, objetivo):
    """BFS: cola (FIFO), por niveles. Da el camino mas corto."""
    cola = deque([(inicio, [inicio])])
    visitados = {inicio}
    recorrido = []
    while cola:
        nodo, camino = cola.popleft()
        arranque = f"Empiezo en {nodo}. " if not recorrido else ""
        if nodo == objetivo:
            recorrido.append({
                "nodo": nodo, "sacado": nodo, "linea": 3,
                "estructura": [n for n, _ in cola],
                "texto": f"{arranque}Saco {nodo} de la cola: es el objetivo. ¡Encontrado!"})
            return {
                "encontrado": True, "camino": camino, "recorrido": recorrido,
                "resumen": f"Llegué a {objetivo} por el camino {' → '.join(camino)} "
                           f"({len(camino) - 1} salto(s)). BFS revisa por niveles, así que "
                           f"este es el camino más corto.",
            }
        nuevos = [v for v in grafo.get(nodo, []) if v not in visitados]
        if nuevos:
            linea = 5
            texto = (f"{arranque}Saco {nodo} del frente de la cola: no es {objetivo}. "
                     f"Encolo sus vecinos nuevos ({', '.join(nuevos)}) al final: primero "
                     f"reviso todo lo cercano antes de alejarme.")
        elif cola:
            linea = 4
            texto = (f"{arranque}Saco {nodo}: no es {objetivo} y no tiene vecinos nuevos. "
                     f"Paso al siguiente de la cola, {cola[0][0]}.")
        else:
            linea = 6
            texto = (f"{arranque}Saco {nodo}: no es {objetivo}, no tiene vecinos nuevos y "
                     f"la cola ya está vacía. No queda nada por explorar.")
        for v in nuevos:
            visitados.add(v)
            cola.append((v, camino + [v]))
        recorrido.append({"nodo": nodo, "sacado": nodo, "linea": linea,
                          "estructura": [n for n, _ in cola], "texto": texto})
    orden = ", ".join(p["nodo"] for p in recorrido)
    return {
        "encontrado": False, "camino": [], "recorrido": recorrido,
        "resumen": f"Revisé todo lo que se puede alcanzar desde {inicio} ({orden}) y la cola "
                   f"quedó vacía sin toparme con {objetivo}. "
                   + _por_que_no(grafo, inicio, objetivo),
    }


# ---------- Benchmark: cuenta comparaciones reales en listas aleatorias ----------
def benchmark(maximo):
    """Lineal (lista desordenada) vs binaria (lista ordenada), enteros aleatorios.
    Por tamaño: 40 objetivos presentes + 40 ausentes. Semilla fija = resultados repetibles."""
    rng = random.Random(42)
    filas = []
    for n in (10, 100, 1000, 10000, 100000):
        if n > maximo:
            break
        base = rng.sample(range(0, n * 4, 2), n)           # pares, sin repetir, desordenados
        ordenada = sorted(base)
        objetivos = rng.sample(base, min(40, n)) + [rng.randrange(1, n * 4, 2) for _ in range(40)]
        lin, bin_ = [], []
        for t in objetivos:
            c = 0
            for x in base:
                c += 1
                if x == t:
                    break
            lin.append(c)
            c, izq, der = 0, 0, n - 1
            while izq <= der:
                c += 1
                mid = (izq + der) // 2
                if ordenada[mid] == t:
                    break
                if ordenada[mid] < t:
                    izq = mid + 1
                else:
                    der = mid - 1
            bin_.append(c)
        filas.append({
            "n": n,
            "lineal_prom": sum(lin) / len(lin), "lineal_peor": max(lin),
            "bin_prom": sum(bin_) / len(bin_), "bin_peor": max(bin_),
        })
    return filas


# ---------- Frontend ----------
HTML = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Algoritmos de búsqueda</title>
<style>
 :root{
  --bg:#fafaf9;--card:#ffffff;--fg:#374151;--tit:#111827;--mut:#9ca3af;--bd:#ececea;
  --ac:#e0e7ff;--ac-h:#c7d2fe;--ac-t:#3730a3;
  --azul-bg:#e0ecff;--azul-bd:#bcd4fb;--azul-t:#1e40af;
  --nar-bg:#fef3c7;--nar-bd:#f6d77a;--nar-t:#92400e;
  --ver-bg:#dcfce7;--ver-bd:#9be4b4;--ver-t:#166534;
  --ros-bg:#fee2e2;--ros-bd:#f7b4b4;--ros-t:#991b1b;
 }
 *{box-sizing:border-box}
 body{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--fg);max-width:1280px;margin:0 auto;padding:2rem 1.25rem 4rem;line-height:1.5}
 h1{font-size:1.4rem;font-weight:600;color:var(--tit);margin:0 0 .2rem;letter-spacing:-.01em}
 .sub{color:var(--mut);margin:0 0 1.25rem;font-size:.9rem}
 .tabs{display:flex;gap:4px;padding:4px;background:#f1f1ef;border-radius:12px;max-width:640px}
 .tab{flex:1;padding:.5rem;border:0;background:transparent;color:var(--fg);border-radius:9px;cursor:pointer;font:inherit;font-size:.9rem;transition:background .15s}
 .tab:hover{background:#e9e9e6}
 .tab.on{background:var(--card);color:var(--tit);font-weight:600;box-shadow:0 1px 2px rgba(0,0,0,.06)}
 .layout{display:grid;grid-template-columns:minmax(340px,460px) minmax(0,1fr);gap:1.25rem;align-items:start;margin-top:1rem}
 @media(max-width:860px){.layout{grid-template-columns:1fr}}
 .card{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:1.25rem}
 .col-izq{position:sticky;top:1rem}
 @media(max-width:860px){.col-izq{position:static}}
 .paso-t{font-size:.75rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin:0 0 .5rem}
 label{display:block;font-weight:500;font-size:.85rem;margin-bottom:.3rem;color:var(--fg)}
 input[type=text]{width:100%;padding:.6rem .75rem;border:1px solid var(--bd);border-radius:10px;background:#fcfcfb;color:var(--tit);font:inherit;transition:border .15s,box-shadow .15s}
 input[type=text]::placeholder{color:#c4c4c0}
 input[type=text]:focus{outline:0;border-color:var(--ac-h);box-shadow:0 0 0 3px var(--ac);background:#fff}
 .ayuda{color:var(--mut);font-size:.8rem;margin:.5rem 0 0}
 .par{display:flex;gap:.5rem;align-items:center}
 .par input{flex:1;min-width:0}
 .flecha{color:var(--mut);font-size:1.1rem}
 .linea{display:flex;gap:.5rem}
 .tipo,.ejemplos{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:.75rem}
 .tipo span,.ejemplos span{font-size:.85rem;font-weight:500;margin-right:.25rem}
 .tipo button,.ejemplos button{padding:.3rem .8rem;border:1px solid var(--bd);background:transparent;color:var(--fg);border-radius:999px;cursor:pointer;font:inherit;font-size:.82rem;transition:all .15s}
 .tipo button:hover,.ejemplos button:hover{background:#f4f4f2}
 .tipo button.on,.ejemplos button.on{background:var(--ac);border-color:var(--ac-h);color:var(--ac-t);font-weight:600}
 .ayuda.err{color:var(--ros-t)}
 .chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:.9rem;min-height:2rem}
 .chip{display:inline-flex;align-items:center;gap:4px;padding:.2rem .3rem .2rem .7rem;border-radius:999px;background:#f4f4f2;font-size:.88rem;color:var(--tit)}
 .chip button{border:0;background:none;color:var(--mut);cursor:pointer;font-size:1rem;line-height:1;padding:0 .35rem;border-radius:50%}
 .chip button:hover{color:var(--ros-t)}
 .vacio{color:var(--mut);font-size:.85rem;align-self:center}
 .placeholder{color:var(--mut);font-size:.9rem;text-align:center;padding:2.5rem 1rem;margin:0}
 .fila{display:flex;gap:.75rem;flex-wrap:wrap;align-items:end}
 .fila>div{flex:1;min-width:120px}
 .btn{padding:.6rem 1.1rem;border:0;border-radius:10px;background:var(--ac);color:var(--ac-t);font:inherit;font-weight:600;font-size:.9rem;cursor:pointer;transition:background .15s;white-space:nowrap}
 .btn:hover{background:var(--ac-h)}
 .btn.sec{background:transparent;color:var(--fg);border:1px solid var(--bd);font-weight:400}
 .btn.sec:hover{background:#f4f4f2}
 .btn.chico{padding:.3rem .8rem;font-size:.8rem}
 .sep{height:1px;background:var(--bd);margin:1.1rem 0}
 .acciones{display:flex;gap:.5rem;margin-top:.9rem;flex-wrap:wrap;align-items:center}
 .acciones label{margin:0;font-weight:400;color:var(--mut);font-size:.85rem;display:flex;align-items:center;gap:.4rem}
 input[type=checkbox]{accent-color:#818cf8}
 input[type=range]{accent-color:#818cf8;width:110px}
 .oculto{display:none!important}
 svg{width:100%;height:auto;display:block;margin:0 auto}
 .cab{display:flex;justify-content:space-between;align-items:center;min-height:1.5rem;margin-bottom:.5rem}
 #msg{font-size:.8rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
 .lista{display:flex;flex-wrap:wrap;gap:6px}
 .item{min-width:48px;text-align:center;padding:.4rem .6rem;border:1.5px solid var(--bd);border-radius:10px;transition:all .25s;background:#fcfcfb;color:var(--tit)}
 .item small{display:block;font-size:.68rem;color:var(--mut)}
 .item.vis{background:var(--azul-bg);border-color:var(--azul-bd);color:var(--azul-t)}
 .item.act{background:var(--nar-bg);border-color:var(--nar-bd);color:var(--nar-t);transform:scale(1.08)}
 .item.ok{background:var(--ver-bg);border-color:var(--ver-bd);color:var(--ver-t);transform:scale(1.08)}
 .item.fuera{opacity:.3}
 .item.vis small,.item.act small,.item.ok small{color:inherit;opacity:.7}
 .leyenda{display:flex;gap:1rem;flex-wrap:wrap;font-size:.78rem;color:var(--mut);margin-top:.75rem}
 .leyenda i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:-1px}
 .log{list-style:none;margin:1rem 0 0;padding:0;display:flex;flex-direction:column;gap:6px}
 .log li{display:flex;gap:.7rem;padding:.6rem .8rem;border:1px solid var(--bd);border-radius:12px;font-size:.88rem;color:var(--mut);background:#fcfcfb;animation:ent .3s ease}
 .log li b{flex:none;width:1.5rem;height:1.5rem;border-radius:50%;background:#f1f1ef;color:var(--mut);display:flex;align-items:center;justify-content:center;font-size:.75rem}
 .log li.now{background:var(--nar-bg);border-color:var(--nar-bd);color:#78350f}
 .log li.now b{background:#fff;color:var(--nar-t)}
 .log li.ok{background:var(--ver-bg);border-color:var(--ver-bd);color:#14532d}
 .log li.ok b{background:#fff;color:var(--ver-t)}
 .log li.pre{background:transparent;border-style:dashed}
 @keyframes ent{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
 .final{margin-top:1rem;padding:1rem 1.1rem;border-radius:14px;font-size:.92rem}
 .final h3{margin:0 0 .25rem;font-size:1rem}
 .final p{margin:0}
 .final.ok{background:var(--ver-bg);color:#14532d;border:1px solid var(--ver-bd)}
 .final.no{background:var(--ros-bg);color:#7f1d1d;border:1px solid var(--ros-bd)}
 select{padding:.6rem .75rem;border:1px solid var(--bd);border-radius:10px;background:#fcfcfb;color:var(--tit);font:inherit}
 select:focus{outline:0;border-color:var(--ac-h);box-shadow:0 0 0 3px var(--ac)}
 .ctrl{display:flex;gap:6px;align-items:center;margin:.25rem 0 1rem;flex-wrap:wrap}
 .ctrl .btn.chico{min-width:2.3rem}
 .ctrl input[type=range]{flex:1;min-width:120px;width:auto}
 .paneles{display:grid;gap:1rem}
 .paneles.dos{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
 .panel{min-width:0}
 .paneles.dos .panel{border:1px solid var(--bd);border-radius:14px;padding:1rem}
 .p-cab{margin-bottom:.6rem}
 .p-cab h3{margin:0;font-size:1.05rem;color:var(--tit)}
 .cx{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
 .cx div{background:#f7f7f5;border-radius:10px;padding:.35rem .4rem;text-align:center}
 .cx small{display:block;font-size:.62rem;color:var(--mut);text-transform:uppercase;letter-spacing:.05em}
 .cx b{font-size:.84rem;color:var(--tit);font-weight:600}
 .nota{color:var(--mut);font-size:.8rem;margin:.5rem 0 .75rem}
 .stats{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:.75rem}
 .stats span{background:var(--ac);color:var(--ac-t);border-radius:999px;padding:.15rem .65rem;font-size:.78rem;font-weight:600}
 .cel{display:flex;flex-direction:column;align-items:center;gap:2px}
 .ptr{font-size:.66rem;font-weight:700;color:var(--nar-t);min-height:1em;line-height:1}
 .estr{margin-top:.75rem;padding:.6rem .75rem;border:1px dashed var(--bd);border-radius:12px;background:#fcfcfb}
 .estr-top{display:flex;gap:.6rem;align-items:baseline;margin-bottom:.4rem;font-size:.78rem}
 .estr-t{font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--mut)}
 .sacado{color:var(--nar-t);font-weight:600}
 .estr-fila{display:flex;gap:5px;flex-wrap:wrap;align-items:center;min-height:2rem}
 .estr-fila small{color:var(--mut);font-size:.68rem}
 .cajita{min-width:2rem;text-align:center;padding:.2rem .5rem;border-radius:8px;background:var(--azul-bg);border:1px solid var(--azul-bd);color:var(--azul-t);font-size:.82rem;font-weight:600}
 .pseudo{margin:.75rem 0 0;padding:.5rem;border:1px solid var(--bd);border-radius:12px;background:#fcfcfb;font:.78rem/1.55 ui-monospace,Consolas,monospace;color:var(--mut);overflow-x:auto}
 .pseudo div{white-space:pre;padding:0 .5rem;border-radius:6px}
 .pseudo div.on{background:var(--nar-bg);color:#78350f}
 .pseudo div.on.ok{background:var(--ver-bg);color:#14532d}
 .log{max-height:260px;overflow-y:auto}
 .log li{animation:none}
 .comp{margin-top:1rem;padding:1rem;border:1px solid var(--ac-h);background:#f5f6ff;border-radius:14px}
 .comp h3{margin:0 0 .5rem;font-size:1rem;color:var(--tit)}
 .tbl{width:100%;border-collapse:collapse;font-size:.85rem}
 .tbl th,.tbl td{text-align:left;padding:.35rem .5rem;border-bottom:1px solid var(--bd)}
 .tbl th{font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);font-weight:600}
 .comp p{margin:.6rem 0 0;font-size:.88rem}
 .bench{margin-top:1rem}
 .bench .ayuda{margin-bottom:.9rem}
 .bn-chart{margin-top:1rem}
 .bn-chart svg{max-width:640px}
</style></head><body>
<h1>Algoritmos de búsqueda</h1>
<p class="sub">Agrega datos, elige un algoritmo y mira qué hace en cada paso.</p>

<div class="tabs" id="tabs">
 <button class="tab on" data-a="lineal">Lineal</button>
 <button class="tab" data-a="binaria">Binaria</button>
 <button class="tab" data-a="profundidad">Profundidad</button>
 <button class="tab" data-a="anchura">Anchura</button>
 <button class="tab" data-a="bench">Benchmark</button>
</div>

<div class="layout" id="layout">
 <div class="card col-izq">
  <p class="paso-t" id="lbl">1 · Tus datos</p>

  <div id="in-lista">
   <div class="ejemplos" id="ej-lista">
    <span>Ejemplos</span>
    <button type="button" data-ej="l1">32 enteros</button>
    <button type="button" data-ej="l2">24 decimales</button>
    <button type="button" data-ej="l3">24 países (texto)</button>
    <button type="button" data-ej="l4">20 enteros (no está)</button>
    <button type="button" data-ej="limpiar">Limpiar</button>
   </div>
   <div class="tipo" id="tipo">
    <span>Tipo de dato</span>
    <button data-t="entero" class="on">Entero · int</button>
    <button data-t="decimal">Decimal · float</button>
    <button data-t="texto">Texto · string</button>
   </div>
   <div class="linea">
    <input type="text" id="entrada" autocomplete="off" placeholder="Ej: 7   (varios con coma: 7, 3, 9)">
    <button class="btn" id="add-l">Agregar</button>
   </div>
   <p class="ayuda" id="ayuda-l"></p>
  </div>

  <div id="in-grafo" class="oculto">
   <div class="ejemplos" id="ej-grafo">
    <span>Ejemplos</span>
    <button type="button" data-ej="g1">Rutas aéreas (18 nodos)</button>
    <button type="button" data-ej="g2">Laberinto (18 nodos)</button>
    <button type="button" data-ej="g3">Ciclos y dirección (15 nodos)</button>
    <button type="button" data-ej="g4">Red con isla (16 nodos)</button>
    <button type="button" data-ej="limpiar">Limpiar</button>
   </div>
   <div class="par">
    <input type="text" id="desde" autocomplete="off" placeholder="Desde (ej. A)">
    <span class="flecha" id="flecha">→</span>
    <input type="text" id="hacia" autocomplete="off" placeholder="Hacia (ej. B)">
    <button class="btn" id="add-g">Agregar</button>
   </div>
   <p class="ayuda" id="ayuda-g">Escribe el origen, Enter, el destino y Enter. Deja Hacia vacío para un nodo suelto.</p>
  </div>

  <div class="chips" id="chips"></div>

  <div id="opc-grafo" class="oculto">
   <div class="acciones">
    <label><input type="checkbox" id="sindir"> Conexiones de ida y vuelta (sin dirección)</label>
   </div>
   <div style="margin-top:.5rem"><svg id="prev"></svg></div>
  </div>

  <div class="sep"></div>
  <p class="paso-t">2 · Qué buscar</p>
  <div class="fila">
   <div id="box-inicio" class="oculto">
    <label>Empezar en</label>
    <input type="text" id="inicio" autocomplete="off" placeholder="(primer nodo)">
   </div>
   <div>
    <label>Buscar</label>
    <input type="text" id="objetivo" autocomplete="off" placeholder="Escribe y Enter">
   </div>
   <button class="btn" id="btn">Buscar</button>
  </div>
  <div class="acciones">
   <label><input type="checkbox" id="comparar"> <span id="comp-txt">Comparar con Binaria</span></label>
  </div>
 </div>

 <div class="card" id="res">
  <div class="cab"><span id="msg">Resultado</span></div>
  <div class="ctrl oculto" id="ctrl">
   <button class="btn sec chico" id="b-ini" title="Al inicio">⏮</button>
   <button class="btn sec chico" id="b-ant" title="Paso anterior (←)">◀</button>
   <button class="btn chico" id="b-play">⏸ Pausar</button>
   <button class="btn sec chico" id="b-sig" title="Paso siguiente (→)">▶</button>
   <input type="range" id="barra" min="1" max="1" value="1">
  </div>
  <p class="placeholder" id="placeholder">Presiona <b>Buscar</b> para ver la visualización y cada paso aquí.</p>
  <div class="paneles" id="paneles"></div>
 </div>
</div>

<div class="bench oculto" id="bench">
 <div class="card">
  <p class="paso-t">Benchmark · Lineal vs Binaria</p>
  <p class="ayuda">Cuenta las comparaciones reales en listas de enteros aleatorios. Sin animación: sirve para ver por qué importa O(n) frente a O(log n).</p>
  <div class="fila" style="max-width:420px">
   <div style="flex:0 0 220px">
    <label>Tamaño máximo de la lista</label>
    <select id="bn-max">
     <option value="1000">1 000</option>
     <option value="10000">10 000</option>
     <option value="100000" selected>100 000</option>
    </select>
   </div>
   <button class="btn" id="bn-run">Ejecutar</button>
  </div>
  <div id="bn-out"></div>
 </div>
</div>

<script>
const $ = id => document.getElementById(id);
const NS = "http://www.w3.org/2000/svg";
const sleep = ms => new Promise(r => setTimeout(r, ms));
// colores de nodos (tonos claros)
const C = {
  borde:"#d6d3d1", arista:"#d6d3d1", ruta:"#86d6a3", ini:"#a5b4fc", texto:"#374151", num:"#94a3b8",
  vis:["#e0ecff","#bcd4fb","#1e40af"], act:["#fef3c7","#f6d77a","#92400e"], ok:["#dcfce7","#86d6a3","#166534"]
};
let modo = "lineal";
let valores = [];
let items = [];                                // [a,b] o [a]
let tipo = "entero";
let corrida = 0;
const esLista = () => modo === "lineal" || modo === "binaria";

/* ---------- Ejemplos ---------- */
const EJEMPLOS_LISTA = {
  l1: {
    tipo: "entero",
    datos: [
      "142", "-18", "67", "9", "215", "34", "88", "0", "-45", "119",
      "53", "76", "21", "184", "62", "11", "-7", "163", "49", "91",
      "28", "130", "83", "5", "197", "72", "39", "108", "156", "94",
      "15", "240"
    ],
    objetivo: "94"
  },
  l2: {
    tipo: "decimal",
    datos: [
      "19.99", "4.50", "85.00", "12.75", "149.90", "3.25", "64.80", "29.95",
      "110.40", "7.99", "49.95", "92.10", "15.60", "210.00", "38.25", "74.50",
      "6.40", "125.99", "55.00", "18.30", "99.95", "41.70", "165.20", "23.45"
    ],
    objetivo: "49.95"
  },
  l3: {
    tipo: "texto",
    datos: [
      "Japón", "Brasil", "Canadá", "Noruega", "Argentina", "Egipto",
      "Francia", "Grecia", "India", "México", "Perú", "Suecia",
      "Turquía", "Vietnam", "Zimbabue", "Dinamarca", "Hungría", "Kenia",
      "Líbano", "Omán", "Qatar", "Rusia", "Uruguay", "Yemen"
    ],
    objetivo: "Noruega"
  },
  l4: {
    tipo: "entero",
    datos: [
      "12", "44", "7", "89", "23", "61", "35", "98", "16", "74",
      "52", "3", "81", "29", "67", "41", "93", "19", "58", "85"
    ],
    objetivo: "55"
  }
};

const EJEMPLOS_GRAFO = {
  g1: {
    sindir: false,
    inicio: "MEX",
    objetivo: "TYO",
    aristas: [
      ["MEX","BOG"], ["BOG","LIM"], ["LIM","SCL"], ["SCL","EZE"], ["EZE","GRU"],
      ["GRU","MAD"], ["MAD","PAR"], ["PAR","LON"], ["LON","TYO"],
      ["LIM","BOG"], ["BOG","PTY"], ["PTY","MIA"], ["MIA","JFK"], ["JFK","LON"],
      ["MEX","GDL"], ["GDL","TIJ"], ["GDL","CUN"],
      ["MEX","MTY"], ["MTY","LAX"], ["LAX","TYO"]
    ]
  },
  g2: {
    sindir: false,
    inicio: "INI",
    objetivo: "META",
    aristas: [
      ["INI","N1"], ["N1","N2"], ["N2","N3"], ["N3","N4"], ["N4","N5"], ["N4","N9"],
      ["N2","N6"], ["N6","N7"], ["N7","N1"], ["N6","N8"],
      ["INI","S1"], ["S1","S2"], ["S2","S3"], ["S3","S5"], ["S3","S4"], ["S4","META"],
      ["INI","D1"], ["D1","D2"], ["D2","META"], ["S2","D2"]
    ]
  },
  g3: {
    sindir: false,
    inicio: "CORE",
    objetivo: "APP",
    aristas: [
      ["CORE","AUTH"], ["AUTH","DB"], ["DB","CACHE"], ["CACHE","AUTH"],
      ["DB","API"], ["API","WEB"], ["WEB","API"], ["API","CDN"], ["CDN","EDGE"],
      ["CORE","LOG"], ["LOG","MON"], ["MON","ALERT"], ["ALERT","LOG"],
      ["MON","QUEUE"], ["APP","QUEUE"], ["APP","SDK"], ["SDK","CLI"]
    ]
  },
  g4: {
    sindir: false,
    inicio: "R1",
    objetivo: "X4",
    aristas: [
      ["R1","R2"], ["R1","R3"],
      ["R2","R4"], ["R2","R5"], ["R3","R5"], ["R3","R6"],
      ["R4","R7"], ["R5","R7"], ["R5","R8"], ["R6","R8"],
      ["R7","R9"], ["R8","R9"], ["R8","R10"], ["R9","R11"], ["R10","R11"],
      ["X1","X2"], ["X2","X3"], ["X3","X4"], ["X4","X1"], ["X3","X5"]
    ]
  }
};

function marcarEjemplo(contId, clave) {
  document.querySelectorAll(`#${contId} button`).forEach(b => b.classList.toggle("on", b.dataset.ej === clave));
}

function cargarEjemploLista(clave) {
  if (clave === "limpiar") {
    valores = [];
    $("objetivo").value = "";
    marcarEjemplo("ej-lista", "");
    limpiarRes(); pintarChips(); aviso("");
    return;
  }
  const ej = EJEMPLOS_LISTA[clave];
  if (!ej) return;
  tipo = ej.tipo;
  valores = [...ej.datos];
  $("objetivo").value = ej.objetivo;
  marcarEjemplo("ej-lista", clave);
  limpiarRes(); actualizarTipo(); pintarChips();
}

function cargarEjemploGrafo(clave) {
  const ayuda = $("ayuda-g");
  ayuda.textContent = "Escribe el origen, Enter, el destino y Enter. Deja Hacia vacío para un nodo suelto.";
  if (clave === "limpiar") {
    items = [];
    $("inicio").value = "";
    $("objetivo").value = "";
    marcarEjemplo("ej-grafo", "");
    limpiarRes(); pintarChips(); previa();
    return;
  }
  const ej = EJEMPLOS_GRAFO[clave];
  if (!ej) return;
  items = ej.aristas.map(par => [...par]);
  $("sindir").checked = !!ej.sindir;
  $("flecha").textContent = ej.sindir ? "↔" : "→";
  $("inicio").value = ej.inicio;
  $("objetivo").value = ej.objetivo;
  marcarEjemplo("ej-grafo", clave);
  limpiarRes(); pintarChips(); previa();
}

$("ej-lista").onclick = e => { if (e.target.dataset.ej) cargarEjemploLista(e.target.dataset.ej); };
$("ej-grafo").onclick = e => { if (e.target.dataset.ej) cargarEjemploGrafo(e.target.dataset.ej); };

/* ---------- Tipo de dato ---------- */
const TIPOS = {
  entero:  {nombre: "un número entero",  ok: /^-?\d+$/,           perm: "0-9\\-",   ej: "7",    modo: "numeric"},
  decimal: {nombre: "un número decimal", ok: /^-?\d+(\.\d+)?$/,  perm: "0-9.\\-",  ej: "3.5",  modo: "decimal"},
  texto:   {nombre: "texto",             ok: /^.+$/,              perm: null,        ej: "hola", modo: "text"}
};
const valido = v => TIPOS[tipo].ok.test(v);
function aviso(t) {
  const a = $("ayuda-l");
  a.textContent = t || ("Tipo " + tipo + ": escribe " + TIPOS[tipo].nombre + " y presiona Enter. Varios separados por coma.");
  a.classList.toggle("err", !!t);
}
function actualizarTipo() {
  const T = TIPOS[tipo];
  document.querySelectorAll("#tipo button").forEach(b => b.classList.toggle("on", b.dataset.t === tipo));
  $("entrada").placeholder = "Ej: " + T.ej + "   (varios con coma)";
  $("entrada").inputMode = T.modo;
  $("objetivo").placeholder = esLista() ? "Ej: " + T.ej : "Escribe y Enter";
  $("objetivo").inputMode = esLista() ? T.modo : "text";
  aviso("");
}
function filtrar(inp, coma) {                  // borra lo que no corresponde al tipo, al escribir o pegar
  if (!esLista() || !TIPOS[tipo].perm) return;
  const n = inp.value.replace(new RegExp("[^" + TIPOS[tipo].perm + (coma ? ", " : "") + "]", "g"), "");
  if (n !== inp.value) { inp.value = n; aviso("Tipo " + tipo + ": solo se permite " + TIPOS[tipo].nombre + "."); }
}
$("entrada").addEventListener("input", () => filtrar($("entrada"), true));
$("objetivo").addEventListener("input", () => filtrar($("objetivo"), false));
$("tipo").onclick = e => {
  const t = e.target.dataset.t; if (!t || t === tipo) return;
  tipo = t;
  marcarEjemplo("ej-lista", "");
  const antes = valores.length;
  valores = valores.filter(valido);            // quita lo que no cabe en el nuevo tipo
  const quitados = antes - valores.length;
  if (!valido($("objetivo").value.trim())) $("objetivo").value = "";
  limpiarRes(); pintarChips(); actualizarTipo();
  if (quitados) aviso(quitados + " valor(es) no eran " + TIPOS[tipo].nombre + " y se quitaron.");
  $("entrada").focus();
};

/* ---------- Modo ---------- */
function ponerModo(m) {
  const eraLista = esLista();
  modo = m;
  const ahoraLista = esLista();
  document.querySelectorAll(".tab").forEach(t => t.classList.toggle("on", t.dataset.a === m));
  $("layout").classList.toggle("oculto", m === "bench");
  $("bench").classList.toggle("oculto", m !== "bench");
  if (m === "bench") { limpiarRes(); return; }
  $("comp-txt").textContent = "Comparar con " + NOMBRES[OTRO[m]];
  $("in-lista").classList.toggle("oculto", !ahoraLista);
  $("in-grafo").classList.toggle("oculto", ahoraLista);
  $("opc-grafo").classList.toggle("oculto", ahoraLista);
  $("box-inicio").classList.toggle("oculto", ahoraLista);
  $("lbl").textContent = ahoraLista ? "1 · Tus valores" : "1 · Tus conexiones";
  limpiarRes();
  if (ahoraLista && !valores.length) {
    cargarEjemploLista("l1");
  } else if (!ahoraLista && !items.length) {
    cargarEjemploGrafo("g1");
  } else if (eraLista !== ahoraLista) {
    $("objetivo").value = "";
    actualizarTipo(); pintarChips(); previa();
  }
  (ahoraLista ? $("entrada") : $("desde")).focus();
}
$("tabs").onclick = e => { if (e.target.dataset.a) ponerModo(e.target.dataset.a); };

function limpiarRes() {
  corrida++; detener();
  if (est && est.resumen) est.resumen.remove();
  est = null;
  $("placeholder").classList.remove("oculto");
  $("paneles").innerHTML = ""; $("paneles").className = "paneles";
  $("msg").textContent = "Resultado";
  $("ctrl").classList.add("oculto");
}

/* ---------- Entrada con Enter ---------- */
function agregar() {
  if (esLista()) {
    const txt = $("entrada").value.trim();
    if (!txt) return;
    const toks = txt.split(",").map(s => s.trim()).filter(Boolean);
    const mal = toks.find(v => !valido(v));
    if (mal !== undefined) { aviso(mal + " no es " + TIPOS[tipo].nombre + "."); return; }
    toks.forEach(v => valores.push(v));
    marcarEjemplo("ej-lista", "");
    aviso("");
    $("entrada").value = ""; $("entrada").focus();
  } else {
    let a = $("desde").value.trim(), b = $("hacia").value.trim();
    if (a && !b) {                         // atajo: "A B", "A,B" o "A>B" en un solo campo
      const t = a.split(/[\s,>\-→]+/).filter(Boolean);
      if (t.length > 2) { $("desde").select(); return; }
      a = t[0]; b = t[1] || "";
    }
    if (!a) { $("desde").focus(); return; }
    items.push(b ? [a, b] : [a]);
    marcarEjemplo("ej-grafo", "");
    $("desde").value = ""; $("hacia").value = ""; $("desde").focus();
  }
  pintarChips(); previa();
}
$("entrada").addEventListener("keydown", e => { if (e.key === "Enter") agregar(); });
$("desde").addEventListener("keydown", e => {
  if (e.key !== "Enter") return;
  const v = $("desde").value.trim();
  if (!v) return;
  if (/[\s,>→-]/.test(v) || $("hacia").value.trim()) agregar(); else $("hacia").focus();
});
$("hacia").addEventListener("keydown", e => {
  if (e.key !== "Enter") return;
  if (!$("desde").value.trim()) { $("desde").focus(); return; }
  agregar();
});
$("add-l").onclick = agregar;
$("add-g").onclick = agregar;
$("objetivo").addEventListener("keydown", e => { if (e.key === "Enter") buscar(); });
$("btn").onclick = buscar;
$("sindir").onchange = () => { $("flecha").textContent = $("sindir").checked ? "↔" : "→"; pintarChips(); previa(); };
$("inicio").oninput = () => previa();

function pintarChips() {
  const c = $("chips"); c.innerHTML = "";
  const sd = $("sindir").checked;
  const lista = esLista() ? valores.map(String)
    : items.map(a => a.length === 2 ? a[0] + (sd ? " ↔ " : " → ") + a[1] : a[0]);
  if (!lista.length) {
    const e = document.createElement("span"); e.className = "vacio";
    e.textContent = esLista() ? "Aún no hay valores." : "Aún no hay conexiones.";
    c.appendChild(e); return;
  }
  lista.forEach((txt, i) => {
    const s = document.createElement("span"); s.className = "chip";
    s.appendChild(document.createTextNode(txt));
    const b = document.createElement("button"); b.textContent = "×"; b.title = "Quitar";
    b.onclick = () => { (esLista() ? valores : items).splice(i, 1); pintarChips(); previa(); };
    s.appendChild(b); c.appendChild(s);
  });
}

/* ---------- Grafo ---------- */
function construirGrafo() {
  const g = {}, sd = $("sindir").checked;
  const add = n => { if (!(n in g)) g[n] = []; };
  items.forEach(([a, b]) => {
    add(a);
    if (b !== undefined) {
      add(b);
      if (!g[a].includes(b)) g[a].push(b);
      if (sd && !g[b].includes(a)) g[b].push(a);
    }
  });
  return g;
}
const nodoInicio = g => $("inicio").value.trim() || Object.keys(g)[0] || "";

function dibujar(svg, g, inicio, est) {
  est = est || {orden: {}, camino: []};
  const sd = $("sindir").checked;
  const nodos = Object.keys(g);
  svg.innerHTML = "";
  if (!nodos.length) { svg.setAttribute("viewBox", "0 0 10 10"); svg.style.maxWidth = "10px"; return; }
  const start = nodos.includes(inicio) ? inicio : nodos[0];

  const nivel = {[start]: 0}, hijos = {};
  nodos.forEach(n => hijos[n] = []);
  const cola = [start];
  while (cola.length) {
    const n = cola.shift();
    for (const h of g[n]) if (!(h in nivel)) { nivel[h] = nivel[n] + 1; hijos[n].push(h); cola.push(h); }
  }
  let hoja = 0; const x = {};
  (function poner(n) {
    if (!hijos[n].length) { x[n] = hoja++; return; }
    hijos[n].forEach(poner);
    x[n] = (x[hijos[n][0]] + x[hijos[n][hijos[n].length - 1]]) / 2;
  })(start);
  // nodos no alcanzables desde el inicial: fila aparte abajo
  const maxN = Math.max(...Object.values(nivel));
  nodos.filter(n => !(n in nivel)).forEach(n => { nivel[n] = maxN + 1; x[n] = hoja++; });

  const DX = 68, DY = 78, R = 21, M = 32;
  const pos = n => [M + x[n] * DX, M + nivel[n] * DY];
  const W = M * 2 + Math.max(hoja - 1, 0) * DX;
  const H = M * 2 + Math.max(...Object.values(nivel)) * DY;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.style.maxWidth = Math.max(W, 120) + "px";

  const el = (tag, at, txt) => {
    const e = document.createElementNS(NS, tag);
    for (const k in at) e.setAttribute(k, at[k]);
    if (txt !== undefined) e.textContent = txt;
    svg.appendChild(e); return e;
  };
  const defs = el("defs", {});
  [["fl", C.arista], ["flc", C.ruta]].forEach(([id, col]) => {
    const m = document.createElementNS(NS, "marker");
    m.setAttribute("id", id + (svg.id || "r")); m.setAttribute("viewBox", "0 0 10 10");
    m.setAttribute("refX", "10"); m.setAttribute("refY", "5");
    m.setAttribute("markerWidth", "9"); m.setAttribute("markerHeight", "9");
    m.setAttribute("markerUnits", "userSpaceOnUse");
    m.setAttribute("orient", "auto");
    const p = document.createElementNS(NS, "path");
    p.setAttribute("d", "M0,0 L10,5 L0,10 z"); p.setAttribute("fill", col);
    m.appendChild(p); defs.appendChild(m);
  });

  const cam = new Set();
  for (let i = 0; i + 1 < (est.camino || []).length; i++) {
    cam.add(est.camino[i] + ">" + est.camino[i + 1]);
    if (sd) cam.add(est.camino[i + 1] + ">" + est.camino[i]);
  }
  for (const a of nodos) for (const b of g[a]) {
    if (sd && a > b && g[b].includes(a)) continue;      // una sola linea si es ida y vuelta
    const [x1, y1] = pos(a), [x2, y2] = pos(b);
    const d = Math.hypot(x2 - x1, y2 - y1) || 1, ux = (x2 - x1) / d, uy = (y2 - y1) / d;
    const en = cam.has(a + ">" + b);
    const at = {
      x1: x1 + ux * R, y1: y1 + uy * R, x2: x2 - ux * (R + (sd ? 0 : 2)), y2: y2 - uy * (R + (sd ? 0 : 2)),
      stroke: en ? C.ruta : C.arista, "stroke-width": en ? 3.5 : 1.5, "stroke-linecap": "round"
    };
    if (!sd) at["marker-end"] = `url(#${en ? "flc" : "fl"}${svg.id || "r"})`;
    el("line", at);
  }
  for (const n of nodos) {
    const [cx, cy] = pos(n);
    let fill = "#ffffff", stroke = C.borde, tx = C.texto, sw = 1.8;
    const o = est.orden[n];
    if (n === est.objetivo && est.encontrado) [fill, stroke, tx] = C.ok;
    else if (n === est.actual) [fill, stroke, tx] = C.act;
    else if (o !== undefined) [fill, stroke, tx] = C.vis;
    else if (n === start) { stroke = C.ini; sw = 3; }
    el("circle", {cx, cy, r: R, fill, stroke, "stroke-width": sw});
    const fs = n.length >= 4 ? 11 : n.length === 3 ? 13 : 15;
    const t = el("text", {x: cx, y: cy + Math.round(fs * 0.35), "text-anchor": "middle", "font-size": fs, "font-weight": 600}, n);
    t.style.fill = tx;
    if (o !== undefined) el("text", {x: cx + R - 2, y: cy - R + 3, "text-anchor": "middle", "font-size": 11, "font-weight": 600}, o).style.fill = C.num;
  }
}
function previa() {
  if (esLista()) return;
  const g = construirGrafo();
  dibujar($("prev"), g, nodoInicio(g));
}

/* ---------- Resultados: paneles + control de pasos ---------- */
const NOMBRES = {lineal: "Lineal", binaria: "Binaria", profundidad: "Profundidad", anchura: "Anchura"};
const OTRO = {lineal: "binaria", binaria: "lineal", profundidad: "anchura", anchura: "profundidad"};
const PASO_MS = 1500;
let est = null, timer = null;

function mk(tag, cls, txt) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (txt !== undefined) e.textContent = txt;
  return e;
}
function detener() { if (timer) { clearInterval(timer); timer = null; } }
function etiquetaPlay() {
  $("b-play").textContent = timer ? "⏸ Pausar" : (est && est.paso >= est.max ? "↻ Repetir" : "▶ Reproducir");
}
function pausar() { detener(); etiquetaPlay(); }
function reproducir() {
  detener();
  timer = setInterval(() => {
    if (!est || est.paso >= est.max) return pausar();
    ir(est.paso + 1);
    if (est.paso >= est.max) pausar();
  }, PASO_MS);
  etiquetaPlay();
}
function errorRes(t) {
  $("placeholder").classList.add("oculto");
  const f = mk("div", "final no");
  f.append(mk("h3", "", "Falta algo"), mk("p", "", t));
  const c = $("paneles"); c.innerHTML = ""; c.className = "paneles"; c.appendChild(f);
}

function crearPanel(d, k, ctx) {
  const lista = d.algo === "lineal" || d.algo === "binaria";
  const info = d.info;
  const el = mk("section", "panel");
  const cab = mk("div", "p-cab"); cab.appendChild(mk("h3", "", info.nombre));
  const cx = mk("div", "cx");
  [["Mejor", info.mejor], ["Promedio", info.promedio], ["Peor", info.peor], ["Memoria", info.memoria]].forEach(([t, v]) => {
    const c = mk("div"); c.append(mk("small", "", t), mk("b", "", v)); cx.appendChild(c);
  });
  const p = {d, el, algo: d.algo, esLista: lista, lineas: []};
  p.stats = mk("div", "stats");
  p.vista = mk("div");
  if (lista) {
    p.base = d.ordenada || ctx.lista;
    p.cont = mk("div", "lista"); p.vista.appendChild(p.cont);
  } else {
    p.totalNodos = Object.keys(ctx.g).length;
    p.svg = document.createElementNS(NS, "svg"); p.svg.id = "res-svg" + k; p.vista.appendChild(p.svg);
    p.estr = mk("div", "estr");
  }
  const ley = mk("div", "leyenda");
  const leyenda = lista ? [["#f6d77a", "actual"], ["#bcd4fb", "en rango / revisado"], ["#86d6a3", "encontrado"]]
                        : [["#a5b4fc", "inicio"], ["#f6d77a", "actual"], ["#bcd4fb", "visitado"], ["#86d6a3", "encontrado"]];
  leyenda.forEach(([c, t]) => { const s = mk("span"); const i = mk("i"); i.style.background = c; s.append(i, t); ley.appendChild(s); });
  const pseudo = mk("div", "pseudo");
  info.pseudo.forEach(t => { const l = mk("div", "", t); pseudo.appendChild(l); p.lineas.push(l); });
  p.log = mk("ol", "log");
  p.fin = mk("div", "final oculto");
  el.append(cab, cx, mk("p", "nota", info.nota), p.stats, p.vista);
  if (p.estr) el.appendChild(p.estr);
  el.append(ley, pseudo, p.log, p.fin);
  return p;
}

function pintarEstr(p, st) {
  const e = p.estr, pila = p.algo === "profundidad";
  e.innerHTML = "";
  const top = mk("div", "estr-top");
  top.append(mk("span", "estr-t", pila ? "Pila" : "Cola"), mk("span", "sacado", "sacó " + st.sacado));
  const fila = mk("div", "estr-fila");
  fila.appendChild(mk("small", "", pila ? "fondo" : "frente"));
  if (!st.estructura.length) fila.appendChild(mk("span", "vacio", "vacía"));
  st.estructura.forEach(x => fila.appendChild(mk("span", "cajita", x)));
  fila.appendChild(mk("small", "", pila ? "tope" : "final"));
  e.append(top, fila);
}

function pintar(p, s) {
  const d = p.d, ctx = est.ctx, n = d.recorrido.length;
  const i = Math.min(s, n) - 1, st = d.recorrido[i];
  const fin = s >= n, ok = fin && d.encontrado;

  p.stats.innerHTML = "";
  const chips = p.esLista
    ? ["Comparaciones: " + (i + 1), "Elementos: " + p.base.length]
    : ["Visitados: " + (i + 1), "En " + (p.algo === "profundidad" ? "pila" : "cola") + ": " + st.estructura.length, "Nodos: " + p.totalNodos];
  if (fin) chips.push(d.encontrado ? "Encontrado" : "No está");
  chips.forEach(t => p.stats.appendChild(mk("span", "", t)));

  if (p.esLista) {
    const marcas = {};
    const poner = (j, t) => (marcas[j] = marcas[j] || []).push(t);
    if (!(fin && !d.encontrado)) {
      if (p.algo === "binaria") { poner(st.rango[0], "izq"); poner(st.rango[1], "der"); poner(st.indice, "mid"); }
      else poner(st.indice, "i");
    }
    const ORD = ["izq", "mid", "der", "i"];
    p.cont.innerHTML = "";
    p.base.forEach((v, j) => {
      let cl = "item";
      if (p.algo === "lineal") { if (j < i) cl += " vis"; }
      else if (st.rango && (j < st.rango[0] || j > st.rango[1])) cl += " fuera";
      else cl += " vis";
      if (j === st.indice) cl = "item " + (ok ? "ok" : "act");
      if (fin && !d.encontrado) cl = "item vis";
      const cel = mk("div", "cel");
      cel.appendChild(mk("span", "ptr", (marcas[j] || []).sort((a, b) => ORD.indexOf(a) - ORD.indexOf(b)).join("·")));
      const it = mk("div", cl, v);
      it.appendChild(mk("small", "", "[" + j + "]"));
      cel.appendChild(it); p.cont.appendChild(cel);
    });
  } else {
    const orden = {};
    for (let j = 0; j <= i; j++) orden[d.recorrido[j].nodo] = j + 1;
    dibujar(p.svg, ctx.g, ctx.inicio, {orden, actual: ok ? null : st.nodo, objetivo: ctx.objetivo, encontrado: ok, camino: ok ? d.camino : []});
    pintarEstr(p, st);
  }

  p.lineas.forEach((l, j) => { l.classList.toggle("on", j === st.linea); l.classList.toggle("ok", ok && j === st.linea); });

  p.log.innerHTML = "";
  if (d.intro) { const li = mk("li", "pre"); li.append(mk("b", "", "·"), mk("span", "", d.intro)); p.log.appendChild(li); }
  for (let j = 0; j <= i; j++) {
    const li = mk("li", j === i ? (ok ? "ok" : "now") : "");
    li.append(mk("b", "", j + 1), mk("span", "", d.recorrido[j].texto));
    p.log.appendChild(li);
  }
  p.log.scrollTop = p.log.scrollHeight;

  if (fin) {
    p.fin.className = "final " + (d.encontrado ? "ok" : "no");
    p.fin.innerHTML = "";
    const titulo = d.encontrado ? (p.esLista ? "Encontrado en la posición " + d.indice : "Encontrado") : ctx.objetivo + " no está";
    p.fin.append(mk("h3", "", titulo), mk("p", "", d.resumen));
  } else {
    p.fin.className = "final oculto";
  }
}

function ir(s) {
  s = Math.max(1, Math.min(est.max, s));
  est.paso = s;
  $("barra").value = s;
  $("msg").textContent = "Paso " + s + " de " + est.max;
  est.paneles.forEach(p => pintar(p, s));
  if (est.resumen) est.resumen.classList.toggle("oculto", s < est.max);
  etiquetaPlay();
}

function resumenComparativo(datos, ctx) {
  const lista = ctx.lista !== undefined;
  const box = mk("div", "comp oculto");
  box.appendChild(mk("h3", "", "Comparación"));
  const t = mk("table", "tbl");
  const fila = (celdas, th) => { const tr = mk("tr"); celdas.forEach(c => tr.appendChild(mk(th ? "th" : "td", "", c))); t.appendChild(tr); };
  fila(["Algoritmo", lista ? "Comparaciones" : "Nodos visitados", "Resultado", lista ? "Posición" : "Camino"], true);
  datos.forEach(d => fila([
    d.info.nombre, d.recorrido.length, d.encontrado ? "Encontrado" : "No está",
    d.encontrado ? (lista ? String(d.indice) : d.camino.join(" → ") + " (" + (d.camino.length - 1) + " saltos)") : "—"
  ]));
  box.appendChild(t);
  const [a, b] = datos;
  const x = a.recorrido.length, y = b.recorrido.length;
  let nota;
  if (lista) {
    if (x === y) nota = "Ambos necesitaron los mismos pasos en este caso.";
    else {
      const [mejor, peor] = x < y ? [a, b] : [b, a];
      const ahorro = Math.round((1 - mejor.recorrido.length / peor.recorrido.length) * 100);
      nota = mejor.info.nombre + " usó " + mejor.recorrido.length + " comparaciones y " + peor.info.nombre + " " + peor.recorrido.length + ": " + ahorro + "% menos. Con listas grandes la diferencia crece mucho (mira la pestaña Benchmark).";
    }
    if (a.encontrado && b.encontrado && a.indice !== b.indice) nota += " La posición difiere porque la binaria trabaja sobre la lista ordenada.";
  } else if (a.encontrado && b.encontrado) {
    const la = a.camino.length - 1, lb = b.camino.length - 1;
    const dfs = a.algo === "profundidad" ? a : b, bfs = dfs === a ? b : a;
    nota = la === lb
      ? "Ambos hallaron un camino de " + la + " saltos. Aquí coinciden; en otros grafos DFS puede dar rodeos."
      : "DFS halló un camino de " + (dfs.camino.length - 1) + " saltos y BFS uno de " + (bfs.camino.length - 1) + ": BFS siempre da el más corto.";
    nota += " Visitaron " + dfs.recorrido.length + " (DFS) y " + bfs.recorrido.length + " (BFS) nodos.";
  } else {
    nota = "Ninguno lo encontró: se exploró todo lo alcanzable desde el nodo inicial.";
  }
  box.appendChild(mk("p", "", nota));
  return box;
}

function iniciar(datos, ctx) {
  $("placeholder").classList.add("oculto");
  const cont = $("paneles"); cont.innerHTML = "";
  cont.className = "paneles" + (datos.length > 1 ? " dos" : "");
  const paneles = datos.map((d, k) => crearPanel(d, k, ctx));
  paneles.forEach(p => cont.appendChild(p.el));
  const max = Math.max(...datos.map(d => d.recorrido.length));
  est = {paneles, ctx, max, paso: 1, resumen: null};
  if (datos.length > 1) { est.resumen = resumenComparativo(datos, ctx); $("res").appendChild(est.resumen); }
  $("barra").max = max;
  $("ctrl").classList.remove("oculto");
  ir(1); reproducir();
}

$("b-ini").onclick = () => { if (est) { pausar(); ir(1); } };
$("b-ant").onclick = () => { if (est) { pausar(); ir(est.paso - 1); } };
$("b-sig").onclick = () => { if (est) { pausar(); ir(est.paso + 1); } };
$("b-play").onclick = () => {
  if (!est) return;
  if (timer) { pausar(); return; }
  if (est.paso >= est.max) ir(1);
  reproducir();
};
$("barra").oninput = () => { if (est) { pausar(); ir(Number($("barra").value)); } };
document.addEventListener("keydown", e => {
  if (!est || (e.key !== "ArrowLeft" && e.key !== "ArrowRight")) return;
  const t = e.target;
  if (t.tagName === "SELECT" || (t.tagName === "INPUT" && (t.type === "text" || t.type === "range"))) return;
  pausar(); ir(est.paso + (e.key === "ArrowRight" ? 1 : -1));
});

/* ---------- Buscar ---------- */
async function buscar() {
  const objetivo = $("objetivo").value.trim();
  limpiarRes();
  const id = corrida;
  if (!objetivo) { errorRes("Escribe qué quieres buscar."); $("objetivo").focus(); return; }

  const base = {objetivo};
  const ctx = {objetivo};
  if (esLista()) {
    if (!valores.length) { errorRes("Agrega al menos un valor."); return; }
    if (!valido(objetivo)) { errorRes(objetivo + " no es " + TIPOS[tipo].nombre + "."); return; }
    base.lista = valores.map(String); base.tipo = tipo;
    ctx.lista = base.lista;
  } else {
    const g = construirGrafo();
    if (!Object.keys(g).length) { errorRes("Agrega al menos una conexión."); return; }
    const inicio = nodoInicio(g);
    if (!(inicio in g)) { errorRes("El nodo inicial " + inicio + " no existe en el grafo."); return; }
    base.grafo = g; base.inicio = inicio;
    ctx.g = g; ctx.inicio = inicio;
  }
  const algos = [modo];
  if ($("comparar").checked) algos.push(OTRO[modo]);
  let datos;
  try {
    datos = await Promise.all(algos.map(a =>
      fetch("/buscar", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({...base, algo: a})}).then(r => r.json())));
  } catch { errorRes("No se pudo conectar con el servidor."); return; }
  if (id !== corrida) return;
  const malo = datos.find(d => d.error);
  if (malo) { errorRes(malo.error); return; }
  iniciar(datos, ctx);
}

/* ---------- Benchmark ---------- */
const fmt = x => x.toLocaleString("es-MX", {maximumFractionDigits: 1});

function pintarBench(filas, out) {
  out.innerHTML = "";
  const W = 600, H = 320, ml = 56, mr = 20, mt = 28, mb = 48;
  const svg = document.createElementNS(NS, "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  const e = (tag, at, txt) => {
    const n = document.createElementNS(NS, tag);
    for (const k in at) n.setAttribute(k, at[k]);
    if (txt !== undefined) n.textContent = txt;
    svg.appendChild(n); return n;
  };
  const dec = Math.max(1, Math.ceil(Math.log10(Math.max(...filas.map(f => f.lineal_peor)))));
  const X = i => ml + (filas.length > 1 ? i * (W - ml - mr) / (filas.length - 1) : (W - ml - mr) / 2);
  const Y = v => mt + (1 - Math.log10(Math.max(v, 1)) / dec) * (H - mt - mb);
  const gris = "#9ca3af";
  e("text", {x: ml, y: 14, "font-size": 11, fill: gris}, "Comparaciones (escala logarítmica)");
  for (let k = 0; k <= dec; k++) {
    const y = Y(Math.pow(10, k));
    e("line", {x1: ml, x2: W - mr, y1: y, y2: y, stroke: "#ececea"});
    e("text", {x: ml - 8, y: y + 4, "text-anchor": "end", "font-size": 11, fill: gris}, fmt(Math.pow(10, k)));
  }
  filas.forEach((f, i) => e("text", {x: X(i), y: H - mb + 20, "text-anchor": "middle", "font-size": 11, fill: gris}, fmt(f.n)));
  e("text", {x: (ml + W - mr) / 2, y: H - 8, "text-anchor": "middle", "font-size": 11, fill: gris}, "Tamaño de la lista (n)");
  const AZ = "#7aa7f0", VE = "#5cc58a";
  [["lineal_peor", AZ, true], ["bin_peor", VE, true], ["lineal_prom", AZ, false], ["bin_prom", VE, false]].forEach(([k, c, punteada]) => {
    e("polyline", {points: filas.map((f, i) => X(i) + "," + Y(f[k])).join(" "), fill: "none", stroke: c,
      "stroke-width": punteada ? 1.5 : 2.5, "stroke-dasharray": punteada ? "5 4" : "none", "stroke-linejoin": "round"});
    if (!punteada) filas.forEach((f, i) => e("circle", {cx: X(i), cy: Y(f[k]), r: 4, fill: c}));
  });
  const caja = mk("div", "bn-chart"); caja.appendChild(svg);
  const ley = mk("div", "leyenda");
  [[AZ, "Lineal · promedio"], [AZ, "Lineal · peor caso (punteada)"], [VE, "Binaria · promedio"], [VE, "Binaria · peor caso (punteada)"]]
    .forEach(([c, t]) => { const s = mk("span"); const i = mk("i"); i.style.background = c; s.append(i, t); ley.appendChild(s); });
  caja.appendChild(ley);
  out.appendChild(caja);

  const t = mk("table", "tbl"); t.style.marginTop = "1rem";
  const fila = (celdas, th) => { const tr = mk("tr"); celdas.forEach(c => tr.appendChild(mk(th ? "th" : "td", "", c))); t.appendChild(tr); };
  fila(["n", "Lineal prom.", "Lineal peor", "Binaria prom.", "Binaria peor", "Ventaja"], true);
  filas.forEach(f => fila([fmt(f.n), fmt(f.lineal_prom), fmt(f.lineal_peor), fmt(f.bin_prom), fmt(f.bin_peor), "×" + fmt(f.lineal_prom / f.bin_prom)]));
  out.appendChild(t);
  out.appendChild(mk("p", "ayuda", "Enteros aleatorios con semilla fija; por tamaño, 40 objetivos presentes y 40 ausentes. Lineal sobre lista desordenada, binaria sobre lista ya ordenada (no cuenta el costo de ordenar). «Ventaja» = comparaciones promedio de lineal ÷ binaria."));
}

$("bn-run").onclick = async () => {
  const out = $("bn-out");
  out.innerHTML = ""; out.appendChild(mk("p", "ayuda", "Calculando…"));
  $("bn-run").disabled = true;
  try {
    const r = await fetch("/benchmark", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({max: Number($("bn-max").value)})});
    const d = await r.json();
    if (d.error) out.textContent = d.error; else pintarBench(d.filas, out);
  } catch { out.textContent = "No se pudo conectar con el servidor."; }
  $("bn-run").disabled = false;
};

cargarEjemploLista("l1");
</script></body></html>
"""


# ---------- Servidor ----------
class Handler(BaseHTTPRequestHandler):
    def _enviar(self, codigo, tipo, datos):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
        self._enviar(200, "text/html; charset=utf-8", HTML.encode("utf-8"))

    def do_POST(self):
        if self.path not in ("/buscar", "/benchmark"):
            return self._enviar(404, "application/json", b"{}")
        try:
            n = int(self.headers.get("Content-Length", 0))
            d = json.loads(self.rfile.read(n))
            if self.path == "/benchmark":
                res = {"filas": benchmark(min(int(d.get("max", 100000)), 100000))}
            else:
                a = d["algo"]
                if a == "lineal":
                    res = busqueda_lineal(d["lista"], d["objetivo"], d.get("tipo", "auto"))
                elif a == "binaria":
                    res = busqueda_binaria(d["lista"], d["objetivo"], d.get("tipo", "auto"))
                elif a == "profundidad":
                    res = busqueda_profundidad(d["grafo"], d["inicio"], d["objetivo"])
                elif a == "anchura":
                    res = busqueda_anchura(d["grafo"], d["inicio"], d["objetivo"])
                else:
                    res = {"error": "Algoritmo desconocido"}
                if "error" not in res:
                    res["algo"] = a
                    res["info"] = INFO[a]
        except Exception as e:
            res = {"error": f"Entrada inválida: {e}"}
        self._enviar(200, "application/json", json.dumps(res).encode("utf-8"))

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print("Servidor en http://localhost:8000  (Ctrl+C para salir)")
    try:
        HTTPServer(("localhost", 8000), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")