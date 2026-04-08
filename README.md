# Tax Evasion and Fraud Detection using Cross-Agency Data Linkage

## 🚀 Overview

This project detects complex tax evasion and fraudulent networks by linking anonymized data from multiple agencies and analyzing relationships using graph analytics.

## 🔍 Features

* Multi-source data integration with privacy-preserving anonymization
* Advanced graph-based fraud detection using NetworkX
* Circular transaction detection and analysis
* Anomaly detection using machine learning (DBSCAN clustering)
* AI-powered analysis assistant providing risk insights and investigative recommendations
* Interactive Streamlit dashboard with network visualization
* Comprehensive fraud risk assessment and reporting

## 🛠️ Tech Stack

* **Python**: Core language for data processing and analysis
* **Pandas**: Data manipulation and analysis
* **NetworkX**: Graph creation and analysis
* **Scikit-learn**: Machine learning for anomaly detection
* **Streamlit**: Interactive web dashboard
* **Matplotlib**: Network visualization
* **Seaborn**: Statistical visualizations

## 📊 How it Works

1. **Data Loading & Anonymization**: Load and anonymize company, transaction, and owner data from multiple sources
2. **Graph Construction**: Build directed graph network from transaction relationships
3. **Advanced Fraud Detection**:
   - Detect circular transactions (potential money laundering)
   - Identify suspicious nodes using centrality measures
   - Apply ML-based anomaly detection (DBSCAN clustering)
4. **AI-Powered Analysis**: Generate intelligent risk assessments and investigative recommendations
5. **Interactive Visualization**: Explore network graphs with color-coded risk levels
6. **Comprehensive Reporting**: Export detailed analysis reports for investigators

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## � Live Demo

[https://sudhar-t10-tax-fraud-detection.streamlit.app](https://sudhar-t10-tax-fraud-detection.streamlit.app)

## 🤖 AI-Powered Analysis Assistant

The system includes an intelligent analysis assistant that provides:

* **Risk Assessment**: Overall fraud risk level based on detected patterns
* **Pattern Explanation**: Detailed explanations of suspicious activities
* **Investigative Recommendations**: Actionable guidance for investigators
* **Network Insights**: Analysis of graph structure and connectivity patterns
* **Confidence Scoring**: AI confidence levels for different detection methods

## 🤖 Future Improvements

* Real-time data integration
* Advanced ML models
* Neo4j graph database
* LLM-powered investigation assistant

## 📝 Code Examples

### Basic App Structure
```python
import streamlit as st

st.title("💰 Tax Fraud Detection System")
st.write("Detect hidden fraud networks using graph analytics and AI")

st.sidebar.header("Options")
option = st.sidebar.selectbox(
    "Choose Analysis",
    ["View Data", "Detect Fraud", "AI Explanation"]
)
```

### Graph Visualization
```python
import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile

# Load data
companies = pd.read_csv('data/companies.csv')
transactions = pd.read_csv('data/transactions.csv')

# Build graph
G = nx.DiGraph()

for _, row in companies.iterrows():
    G.add_node(row['company_id'])

for _, row in transactions.iterrows():
    G.add_edge(row['from_company'], row['to_company'], weight=row['amount'])

# Detect suspicious nodes (simple rule: high degree)
centrality = nx.degree_centrality(G)
suspicious = [node for node, val in centrality.items() if val > 0.5]

# Streamlit UI
st.title("🔗 Fraud Network Visualization")

# Create PyVis graph
net = Network(height="500px", width="100%", directed=True)

for node in G.nodes():
    color = "red" if node in suspicious else "green"
    net.add_node(node, label=node, color=color)

for u, v, data in G.edges(data=True):
    net.add_edge(u, v, title=str(data['weight']))

# Save and display
tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
net.save_graph(tmp_file.name)

st.components.v1.html(open(tmp_file.name, 'r').read(), height=500)
```

*Here we visualize the fraud network as a graph. Each node represents a company, and each edge represents a financial transaction. We highlight suspicious nodes in red based on their connectivity and abnormal behavior. For example, circular transaction patterns indicate potential money laundering or tax evasion. This visualization helps investigators quickly understand complex fraud structures which are not visible in traditional data tables.*

### Advanced Analysis
```python
import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile

st.set_page_config(layout="wide")

st.title("🔍 Advanced Fraud Network Analysis")

# Load data
companies = pd.read_csv('data/companies.csv')
transactions = pd.read_csv('data/transactions.csv')

# Sidebar filters
st.sidebar.header("🔧 Filters")

min_amount = st.sidebar.slider("Minimum Transaction Amount", 0, 20000, 0)

# Filter transactions
filtered_tx = transactions[transactions['amount'] >= min_amount]

# Build graph
G = nx.DiGraph()

for _, row in companies.iterrows():
    G.add_node(row['company_id'])

for _, row in filtered_tx.iterrows():
    G.add_edge(row['from_company'], row['to_company'], weight=row['amount'])

# Fraud detection logic
centrality = nx.degree_centrality(G)
suspicious_nodes = [n for n, v in centrality.items() if v > 0.5]

cycles = list(nx.simple_cycles(G))

# UI Info
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Nodes", len(G.nodes()))
    st.metric("Total Transactions", len(filtered_tx))

with col2:
    st.metric("Suspicious Nodes", len(suspicious_nodes))
    st.metric("Detected Cycles", len(cycles))

# Create PyVis graph
net = Network(height="600px", width="100%", directed=True)

# Add nodes
for node in G.nodes():
    if node in suspicious_nodes:
        net.add_node(node, label=node, color="red", size=25)
    else:
        net.add_node(node, label=node, color="green", size=15)

# Add edges
for u, v, data in G.edges(data=True):
    net.add_edge(u, v, title=f"₹{data['weight']}")

# Physics settings (better layout)
net.repulsion(node_distance=200, central_gravity=0.3)

# Save graph
tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
net.save_graph(tmp_file.name)

# Display graph
st.components.v1.html(open(tmp_file.name, 'r').read(), height=600)

# Show fraud insights
st.write("## 🚨 Fraud Insights")

if cycles:
    st.warning(f"Detected Circular Transactions: {cycles}")

if suspicious_nodes:
    st.error(f"High Risk Nodes: {suspicious_nodes}")

if not cycles and not suspicious_nodes:
    st.success("No major fraud patterns detected")
```

*This is our advanced fraud network visualization dashboard. We allow dynamic filtering of transactions based on value, which helps focus on high-risk financial activities. The system automatically detects suspicious nodes using graph centrality and identifies circular transaction patterns. For example, these cycles represent potential money laundering loops where funds circulate between entities to evade taxes. This interactive visualization enables investigators to explore complex fraud networks efficiently.*

### AI Assistant
```python
import streamlit as st

st.write("## 🤖 AI Fraud Assistant")

user_input = st.text_input("Ask about fraud analysis:")

def simple_ai_response(query, cycles, suspicious_nodes):
    query = query.lower()

    if "why" in query or "suspicious" in query:
        return f"These nodes are suspicious because they have high connectivity and are part of abnormal transaction patterns: {suspicious_nodes}"

    elif "cycle" in query or "fraud" in query:
        return f"Circular transactions detected: {cycles}. This may indicate money laundering."

    elif "risk" in query:
        return f"High risk entities: {suspicious_nodes}"

    else:
        return "Ask about fraud, cycles, or suspicious nodes."

if user_input:
    response = simple_ai_response(user_input, cycles, suspicious_nodes)
    st.success(response)
```

### Risk Score Analysis
```python
from sklearn.ensemble import IsolationForest
import numpy as np

st.write("## 📊 Risk Score Analysis")

# Prepare feature (degree of nodes)
node_list = list(G.nodes())
degrees = np.array([G.degree(n) for n in node_list]).reshape(-1, 1)

# Train model
model = IsolationForest(contamination=0.3)
model.fit(degrees)

scores = model.decision_function(degrees)

risk_scores = {node: round((1 - score) * 100, 2) for node, score in zip(node_list, scores)}

st.write(risk_scores)
```

### Neo4j Integration (Future)
```python
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

def create_graph(tx, companies, transactions):
    for _, row in companies.iterrows():
        tx.run("MERGE (c:Company {id: $id})", id=row['company_id'])

    for _, row in transactions.iterrows():
        tx.run("""
        MATCH (a:Company {id: $from}), (b:Company {id: $to})
        MERGE (a)-[:TRANSACTION {amount: $amt}]->(b)
        """, from=row['from_company'], to=row['to_company'], amt=row['amount'])

with driver.session() as session:
    session.write_transaction(create_graph, companies, transactions)
```