import time
import heapq
from collections import deque

# Grafo
grafo = {
    "S": [("J", 18)],
    "J": [("S", 18), ("F", 22), ("TQ", 16)],
    "TQ": [("J", 16)],

    "F": [
        ("H", 12),
        ("M", 15),
        ("T", 18),
        ("J", 22),
        ("B", 25),
        ("W", 20),
        ("G", 28),
        ("A", 31),
        ("C", 20),
        ("SFe", 20),
        ("Cj", 28)
    ],

    "H": [("F", 12), ("A", 22)],
    "A": [("F", 31), ("H", 22)],

    "M": [("F", 15), ("T", 9), ("W", 12), ("Sg", 20)],
    "T": [("F", 18), ("M", 9), ("I", 26)],
    "I": [("T", 26)],

    "W": [("F", 20), ("M", 12), ("Cj", 22)],

    "Sg": [("M", 20), ("AM", 24)],
    "AM": [("Sg", 24), ("Cj", 24)],

    "Cj": [("F", 28), ("W", 22), ("AM", 24), ("SA", 32)],

    "SA": [("Cj", 32)],

    "B": [("F", 25)],
    "G": [("F", 28)],
    "C": [("F", 20)],
    "SFe": [("F", 20)]
}

# ----------------------------------------------------
# Calcula distância total do caminho
# ----------------------------------------------------
def calcular_distancia(caminho):
    total = 0

    for origem, destino in zip(caminho, caminho[1:]):
        for vizinho, peso in grafo[origem]:
            if vizinho == destino:
                total += peso
                break

    return total


# ----------------------------------------------------
# BFS
# ----------------------------------------------------
def bfs(inicio, fim):

    fila = deque([(inicio, [inicio])])
    visitados = {inicio}

    while fila:

        atual, caminho = fila.popleft()

        if atual == fim:
            return caminho

        for vizinho, peso in grafo[atual]:

            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))

    return None


# ----------------------------------------------------
# DFS
# ----------------------------------------------------
def dfs(inicio, fim):

    pilha = [(inicio, [inicio])]
    visitados = set()

    while pilha:

        atual, caminho = pilha.pop()

        if atual == fim:
            return caminho

        if atual not in visitados:

            visitados.add(atual)

            for vizinho, peso in reversed(grafo[atual]):

                if vizinho not in visitados:
                    pilha.append((vizinho, caminho + [vizinho]))

    return None


# ----------------------------------------------------
# Dijkstra
# ----------------------------------------------------
def dijkstra(inicio, fim):

    fila = [(0, inicio, [inicio])]
    visitados = set()

    while fila:

        custo, atual, caminho = heapq.heappop(fila)

        if atual == fim:
            return caminho, custo

        if atual not in visitados:

            visitados.add(atual)

            for vizinho, peso in grafo[atual]:

                if vizinho not in visitados:

                    heapq.heappush(
                        fila,
                        (custo + peso,
                         vizinho,
                         caminho + [vizinho])
                    )

    return None, None


# ----------------------------------------------------
# Mede média de 100 execuções
# ----------------------------------------------------
def testar_bfs():

    tempos = []

    for _ in range(100):

        t0 = time.perf_counter()

        caminho = bfs("S", "SA")

        tf = time.perf_counter()

        tempos.append(tf - t0)

    if caminho:
        distancia = calcular_distancia(caminho)
    else:
        distancia = None

    return caminho, distancia, sum(tempos)/100


def testar_dfs():

    tempos = []

    for _ in range(100):

        t0 = time.perf_counter()

        caminho = dfs("S", "SA")

        tf = time.perf_counter()

        tempos.append(tf - t0)

    if caminho:
        distancia = calcular_distancia(caminho)
    else:
        distancia = None

    return caminho, distancia, sum(tempos)/100


def testar_dijkstra():

    tempos = []

    for _ in range(100):

        t0 = time.perf_counter()

        caminho, distancia = dijkstra("S", "SA")

        tf = time.perf_counter()

        tempos.append(tf - t0)

    return caminho, distancia, sum(tempos)/100


# ----------------------------------------------------
# EXECUÇÃO
# ----------------------------------------------------
print("=" * 60)
print("RESULTADOS")
print("=" * 60)


def imprimir_resultado(titulo, caminho, distancia, tempo_s):
    print("\n" + titulo)

    if caminho is None:
        print("Nenhum caminho encontrado")
        return

    print("Caminho:", " -> ".join(caminho))

    if distancia is None:
        print("Distância: desconhecida")
    else:
        print("Distância:", distancia, "km")

    print("Tempo médio:", tempo_s * 1000, "ms")


caminho_bfs, dist_bfs, tempo_bfs = testar_bfs()
imprimir_resultado("BFS", caminho_bfs, dist_bfs, tempo_bfs)

caminho_dfs, dist_dfs, tempo_dfs = testar_dfs()
imprimir_resultado("DFS", caminho_dfs, dist_dfs, tempo_dfs)

caminho_dijkstra, dist_dijkstra, tempo_dijkstra = testar_dijkstra()
imprimir_resultado("DIJKSTRA", caminho_dijkstra, dist_dijkstra, tempo_dijkstra)