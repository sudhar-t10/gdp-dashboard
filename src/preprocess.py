import pandas as pd
import hashlib

def anonymize(value):
    return hashlib.sha256(value.encode()).hexdigest()[:8]

def load_data():
    companies = pd.read_csv('data/companies.csv')
    owners = pd.read_csv('data/owners.csv')
    transactions = pd.read_csv('data/transactions.csv')

    # anonymize owner names
    owners['owner_name'] = owners['owner_name'].apply(anonymize)

    return companies, owners, transactions