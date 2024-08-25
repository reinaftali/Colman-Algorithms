import random


# ------------------section:1------------------
def prim(graph, start_node=0):
    V = list(graph.keys())
    Q = set(V)
    key = {u: float('inf') for u in V}
    parent = {u: None for u in V}
    key[start_node] = 0

    def extract_min(Q, key):
        min_node = min(Q, key=lambda node: key[node])
        Q.remove(min_node)
        return min_node

    while Q:
        u = extract_min(Q, key)
        for v, weight in graph[u]:
            if v in Q and weight < key[v]:
                parent[v] = u
                key[v] = weight

    mst = [(parent[v], v, key[v]) for v in V if parent[v] is not None]
    return mst


# ------------------section:2------------------
def update_mst(mst, new_edge):
    def find_cycle(graph, start, end):
        visited = set()
        path = []

        def dfs(node):
            visited.add(node)
            path.append(node)
            if node == end:
                return True
            for neighbor, _ in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
            path.pop()
            return False

        dfs(start)
        return path if path[-1] == end else None

    graph = {}
    for u, v, weight in mst:
        if u not in graph: graph[u] = []
        if v not in graph: graph[v] = []
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    u, v, weight = new_edge
    if u not in graph: graph[u] = []
    if v not in graph: graph[v] = []
    graph[u].append((v, weight))
    graph[v].append((u, weight))

    cycle = find_cycle(graph, u, v)

    if not cycle:
        mst.append(new_edge)
        return mst

    max_edge = max([(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)],
                   key=lambda e: next(w for n, w in graph[e[0]] if n == e[1]))
    max_weight = next(w for n, w in graph[max_edge[0]] if n == max_edge[1])

    if weight < max_weight:
        mst = [edge for edge in mst if set(edge[:2]) != set(max_edge)]
        mst.append(new_edge)

    return mst


# ------------------section:3------------------
def create_graph(num_nodes, num_edges):
    graph = {i: [] for i in range(num_nodes)}
    edges = set()
    while len(edges) < num_edges:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            weight = random.randint(1, 10)
            edges.add((u, v, weight))
            graph[u].append((v, weight))
            graph[v].append((u, weight))
    return graph, edges


def print_graph(graph):
    print("Graph:")
    for u in graph:
        for v, weight in graph[u]:
            print(f"(u:{u}, v:{v}, weight:{weight})")
    print()


def print_mst(mst):
    print("Minimal Spanning Tree:")
    for u, v, weight in mst:
        print(f"(u:{u}, v:{v}, weight:{weight})")
    print()


def main():
    # Create a graph with at least 20 nodes and 50 edges
    num_nodes = 20
    num_edges = 50
    graph, _ = create_graph(num_nodes, num_edges)

    print_graph(graph)

    # Find and print the initial MST
    mst = prim(graph)
    print_mst(mst)

    # Create a new edge that doesn't change the MST
    new_edge = (0, 1, 10)
    print(f"Adding new edge that does not affect MST: {new_edge}")
    updated_mst = update_mst(mst, new_edge)
    print_mst(updated_mst)

    # Create a new edge that does change the MST
    new_edge = (2, 3, 1)
    print(f"Adding new edge that affects MST: {new_edge}")
    updated_mst = update_mst(updated_mst, new_edge)
    print_mst(updated_mst)


if __name__ == "__main__":
    main()
