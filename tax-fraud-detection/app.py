import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from src.preprocess import load_data
from src.graph_builder import build_graph
from src.fraud_detection import detect_cycles, suspicious_nodes
from src.ai_agent import analyze_fraud

st.set_page_config(page_title="Tax Fraud Detection Dashboard", page_icon="🔍", layout="wide")

st.title("🔍 Tax Evasion and Fraud Detection Dashboard")
st.markdown("**Secure, Privacy-Preserving Cross-Agency Data Analysis**")

# Sidebar
st.sidebar.header("📊 Analysis Controls")
run_analysis = st.sidebar.button("🚀 Run Fraud Analysis", type="primary")

# Data Upload Section
st.sidebar.header("📁 Data Upload")
uploaded_companies = st.sidebar.file_uploader("Upload companies.csv", type="csv")
uploaded_transactions = st.sidebar.file_uploader("Upload transactions.csv", type="csv")
uploaded_owners = st.sidebar.file_uploader("Upload owners.csv", type="csv")

use_sample = st.sidebar.checkbox("Use Sample Data", value=True)

if run_analysis:
    with st.spinner("🔄 Analyzing data for fraud patterns..."):
        # Load data
        if use_sample or not (uploaded_companies and uploaded_transactions and uploaded_owners):
            companies, owners, transactions = load_data()
            st.info("Using sample data. Upload files in sidebar to use custom data.")
        else:
            companies = pd.read_csv(uploaded_companies)
            transactions = pd.read_csv(uploaded_transactions)
            owners = pd.read_csv(uploaded_owners)
            # Anonymize owners
            import hashlib
            owners['owner_name'] = owners['owner_name'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest()[:8])

        # Data Overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Companies", companies.shape[0])
        with col2:
            st.metric("Transactions", transactions.shape[0])
        with col3:
            st.metric("Owners (Anonymized)", owners.shape[0])

        # Build graph
        G = build_graph(companies, transactions)

        # Fraud Detection
        cycles = detect_cycles(G)
        suspicious = suspicious_nodes(G)

        # Network Stats
        from src.fraud_detection import network_stats
        stats = network_stats(G)

    # Analysis Results
    st.header("🔍 Fraud Analysis Results")
    result = analyze_fraud(cycles, suspicious)
    st.text_area("Analysis Report", result, height=150)

    # Statistics
    st.header("📈 Network Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Nodes", stats["nodes"])
    with col2:
        st.metric("Total Edges", stats["edges"])
    with col3:
        st.metric("Circular Transactions", len(cycles))
    with col4:
        st.metric("Suspicious Nodes", len(suspicious))

    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Network Density", f"{stats['density']:.3f}")
    with col6:
        st.metric("Avg Clustering", f"{stats['average_clustering']:.3f}")
    with col7:
        st.metric("Connected Components", stats["connected_components"])

    # Graph Visualization
    st.header("🌐 Transaction Network Graph")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Color nodes: red for suspicious, blue for normal
    node_colors = ['red' if node in suspicious else 'lightblue' for node in G.nodes()]

    pos = nx.spring_layout(G, k=1, iterations=50)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=600,
            font_size=8, font_weight='bold', ax=ax, edge_color='gray', width=1.5)

    # Highlight edges in cycles
    if cycles:
        cycle_edges = []
        for cycle in cycles:
            for i in range(len(cycle)):
                cycle_edges.append((cycle[i], cycle[(i+1)%len(cycle)]))
        nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, edge_color='red', width=3, ax=ax)

    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6, ax=ax)

    st.pyplot(fig)

    # Detailed Suspicious Nodes
    if suspicious:
        st.header("🚨 Detailed Suspicious Nodes Analysis")
        suspicious_df = pd.DataFrame(list(suspicious.items()), columns=["Node ID", "Reason"])
        st.dataframe(suspicious_df, use_container_width=True)

    # Export Results
    st.header("💾 Export Results")
    if st.button("Download Analysis Report"):
        st.download_button(
            label="Download as Text",
            data=result,
            file_name="fraud_analysis_report.txt",
            mime="text/plain"
        )

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("This dashboard detects tax evasion patterns using graph analytics on cross-agency data. Built for privacy-preserving fraud detection.")

st.sidebar.markdown("### How it Works")
st.sidebar.markdown("""
1. **Data Loading**: Load anonymized company, transaction, and owner data
2. **Graph Construction**: Build directed graph from transactions
3. **Fraud Detection**: Identify cycles and suspicious nodes
4. **Analysis**: Generate human-readable reports
5. **Visualization**: Interactive network graph
""")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ for tax fraud detection hackathon | Privacy-preserving analytics")