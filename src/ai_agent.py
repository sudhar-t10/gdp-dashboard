def analyze_fraud(cycles, suspicious):
    response = ""

    if cycles:
        response += f"⚠️ Detected circular transactions: {cycles}\n"

    if suspicious:
        response += f"🚨 High-risk nodes: {list(suspicious.keys())}\n"

    if not cycles and not suspicious:
        response = "✅ No major fraud detected"

    return response