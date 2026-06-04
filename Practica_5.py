import matplotlib.pyplot as plt
import math

class UnionFind:
    """
    Estructura de datos Union-Find (Conjuntos Disjuntos).
    Utilizada para administrar los subconjuntos de vértices y detectar ciclos 
    durante la construcción del árbol de expansión.
    """
    def __init__(self, vertices):
        # Cada vértice es inicialmente su propio padre (árboles independientes)
        self.parent = {v: v for v in vertices}
        # El rango ayuda a mantener el árbol plano al hacer las uniones
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        """Busca la raíz del conjunto al que pertenece el elemento, aplicando compresión de ruta."""
        if self.parent[item] == item:
            return item
        self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, x, y):
        """
        Une dos conjuntos. 
        Retorna True si se unieron exitosamente, o False si ya pertenecían al mismo conjunto (ciclo).
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            # Unión por rango para optimizar la altura del árbol
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            return True
        return False

class Graph:
    """
    Representación del grafo mediante una lista de aristas para facilitar el 
    ordenamiento requerido por el algoritmo de Kruskal.
    """
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []

    def add_edge(self, u, v, w):
        """Registra una nueva arista con su peso correspondiente."""
        self.edges.append((w, u, v))

    def kruskal(self, find_max=False):
        """
        Ejecuta el algoritmo de Kruskal.
        :param find_max: Booleano. False para Árbol de Mínimo Coste, True para Máximo Coste.
        :return: Lista de aristas que componen el árbol resultante.
        """
        mst = []
        
        # Ordenamiento de las aristas. Descendente si es Máximo, Ascendente si es Mínimo.
        sorted_edges = sorted(self.edges, key=lambda item: item[0], reverse=find_max)
        uf = UnionFind(self.V)

        # Formato de salida en consola para trazabilidad del algoritmo
        tipo = "MÁXIMO" if find_max else "MÍNIMO"
        print(f"\n{'='*50}")
        print(f" LOG DE EJECUCIÓN: ÁRBOL DE {tipo} COSTE ")
        print(f"{'='*50}")

        total_cost = 0
        for w, u, v in sorted_edges:
            # Se evalúa si la inserción de la arista genera un ciclo
            if uf.union(u, v):
                mst.append((u, v, w))
                total_cost += w
                print(f"[+] Arista unida: ({u} - {v}) | Peso: {w}")
            else:
                print(f"[-] Arista descartada: ({u} - {v}) | Peso: {w} -> Genera ciclo")

        print(f"\n-> Coste total calculado: {total_cost}\n")
        return mst

def draw_graph(vertices, all_edges, tree_edges, title):
    """
    Renderiza el grafo utilizando matplotlib puro.
    Se implementa una distribución circular matemática de los nodos para evitar 
    dependencias de terceros orientadas a grafos.
    """
    pos = {}
    n = len(vertices)
    
    # Cálculo de coordenadas mediante trigonometría básica (distribución circular)
    for i, v in enumerate(vertices):
        angle = 2 * math.pi * i / n
        pos[v] = (math.cos(angle), math.sin(angle))

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Renderizado de la estructura base del grafo (fondo)
    for w, u, v in all_edges:
        x_values = [pos[u][0], pos[v][0]]
        y_values = [pos[u][1], pos[v][1]]
        ax.plot(x_values, y_values, color='lightgray', linestyle='dotted', zorder=1)
        
        # Etiquetas de peso de las aristas
        mid_x = (pos[u][0] + pos[v][0]) / 2
        mid_y = (pos[u][1] + pos[v][1]) / 2
        ax.text(mid_x, mid_y, str(w), color='black', fontsize=10, 
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7),
                ha='center', va='center', zorder=3)

    # Renderizado de las aristas seleccionadas por Kruskal
    color_arista = 'firebrick' if "Máximo" in title else 'forestgreen'
    for u, v, w in tree_edges:
        x_values = [pos[u][0], pos[v][0]]
        y_values = [pos[u][1], pos[v][1]]
        ax.plot(x_values, y_values, color=color_arista, linewidth=3, zorder=2)

    # Renderizado de los vértices (nodos)
    for v in vertices:
        ax.scatter(pos[v][0], pos[v][1], s=800, color='royalblue', edgecolor='black', zorder=4)
        ax.text(pos[v][0], pos[v][1], str(v), fontsize=12, fontweight='bold', color='white', 
                ha='center', va='center', zorder=5)

    ax.axis('off')
    plt.show()

# ==========================================
# Bloque principal de ejecución (Main)
# ==========================================
if __name__ == "__main__":
    # Inicialización de la estructura de datos
    vertices = ['A', 'B', 'C', 'D', 'E', 'F']
    g = Graph(vertices)

    # Carga de matriz de adyacencias / aristas (Origen, Destino, Peso)
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'F', 2)
    g.add_edge('B', 'C', 6)
    g.add_edge('B', 'F', 5)
    g.add_edge('C', 'D', 3)
    g.add_edge('C', 'F', 1)
    g.add_edge('D', 'E', 2)
    g.add_edge('E', 'F', 4)

    # Ejecución y visualización: Kruskal Mínimo Coste
    min_tree = g.kruskal(find_max=False)
    draw_graph(vertices, g.edges, min_tree, "Árbol de Mínimo Coste (Kruskal)")

    # Ejecución y visualización: Kruskal Máximo Coste
    max_tree = g.kruskal(find_max=True)
    draw_graph(vertices, g.edges, max_tree, "Árbol de Máximo Coste (Kruskal)")