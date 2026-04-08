import networkx as nx
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np

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

    # Eigenvector centrality (influence)
    try:
        eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
        for node, cent in eigenvector.items():
            if cent > 0.5:  # High influence
                if node in suspicious:
                    suspicious[node] += f", High influence ({cent:.3f})"
                else:
                    suspicious[node] = f"High influence ({cent:.3f})"
    except:
        pass  # Skip if not applicable

    return suspicious

def detect_anomalies(G):
    """
    Detect anomalous nodes using clustering and centrality measures
    """
    anomalies = {}

    # Extract features for anomaly detection
    degrees = dict(G.degree())
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)

    # Prepare data for clustering
    nodes = list(G.nodes())
    features = []
    for node in nodes:
        features.append([
            degrees.get(node, 0),
            betweenness.get(node, 0),
            closeness.get(node, 0)
        ])

    if len(features) < 2:
        return anomalies

    # Standardize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # DBSCAN clustering for anomaly detection
    dbscan = DBSCAN(eps=0.5, min_samples=2)
    clusters = dbscan.fit_predict(features_scaled)

    # Nodes with -1 are outliers (anomalies)
    for i, node in enumerate(nodes):
        if clusters[i] == -1:
            anomalies[node] = "Anomalous network behavior (outlier detection)"

    return anomalies

def network_stats(G):
    stats = {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": nx.density(G),
        "average_clustering": nx.average_clustering(G),
        "connected_components": nx.number_connected_components(G.to_undirected())
    }
    return stats