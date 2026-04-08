import networkx as nx

def build_graph(companies, transactions):
    G = nx.DiGraph()

    # Add company nodes
    for _, row in companies.iterrows():
        G.add_node(row['company_id'], type='company')

    # Add transaction edges
    for _, row in transactions.iterrows():
        G.add_edge(row['from_company'], row['to_company'], weight=row['amount'])

    return G