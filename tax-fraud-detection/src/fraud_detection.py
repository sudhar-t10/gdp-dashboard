import networkx as nx

def detect_cycles(G):
    try:
        cycles = list(nx.simple_cycles(G))
        return cycles
    except:
        return []

def suspicious_nodes(G, threshold_degree=5, threshold_betweenness=0.1):
    suspicious = {}

    # Degree centrality
    degrees = dict(G.degree())
    for node, deg in degrees.items():
        if deg > threshold_degree:
            suspicious[node] = f"High degree ({deg})"

    # Betweenness centrality
    betweenness = nx.betweenness_centrality(G)
    for node, cent in betweenness.items():
        if cent > threshold_betweenness:
            if node in suspicious:
                suspicious[node] += f", High betweenness ({cent:.3f})"
            else:
                suspicious[node] = f"High betweenness ({cent:.3f})"

    return suspicious

def network_stats(G):
    stats = {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": nx.density(G),
        "average_clustering": nx.average_clustering(G),
        "connected_components": nx.number_connected_components(G.to_undirected())
    }
    return stats