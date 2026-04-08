def analyze_fraud(cycles, suspicious, stats=None):
    """
    AI-powered fraud analysis providing explanations, risk insights, and decision-making support.
    """
    response = "**Fraud Detection Analysis Report**\n\n"

    # Overall Risk Assessment
    risk_level = "Low"
    if len(cycles) > 0 or len(suspicious) > 5:
        risk_level = "High"
    elif len(cycles) > 0 or len(suspicious) > 2:
        risk_level = "Medium"

    response += f"**Overall Risk Level:** {risk_level}\n\n"

    # Circular Transactions Analysis
    if cycles:
        response += f"⚠️ **Circular Transactions Detected:** {len(cycles)} cycle(s) found\n"
        response += "Circular transactions may indicate:\n"
        response += "- Money laundering schemes\n"
        response += "- Tax evasion through artificial loops\n"
        response += "- Shell company networks\n\n"
        for i, cycle in enumerate(cycles[:3]):  # Show first 3 cycles
            response += f"  Cycle {i+1}: {' → '.join(map(str, cycle))}\n"
        if len(cycles) > 3:
            response += f"  ... and {len(cycles)-3} more cycles\n\n"
    else:
        response += "✅ **No circular transactions detected**\n\n"

    # Suspicious Nodes Analysis
    if suspicious:
        response += f"🚨 **High-Risk Entities Identified:** {len(suspicious)} suspicious node(s)\n"
        response += "These entities show unusual network behavior:\n\n"
        for node, reason in list(suspicious.items())[:5]:  # Show top 5
            response += f"- **Node {node}:** {reason}\n"
            response += "  *Investigation Recommendation:* Check ownership, transaction history, and cross-agency records*\n"
        if len(suspicious) > 5:
            response += f"... and {len(suspicious)-5} more suspicious entities\n\n"
    else:
        response += "✅ **No highly suspicious entities detected**\n\n"

    # Network Insights
    if stats:
        response += "**Network Structure Insights:**\n"
        response += f"- Network Density: {stats['density']:.3f} "
        if stats['density'] > 0.1:
            response += "(Dense network - potential coordinated activity)\n"
        else:
            response += "(Sparse network - normal business relationships)\n"

        response += f"- Connected Components: {stats['connected_components']} "
        if stats['connected_components'] > stats['nodes'] * 0.5:
            response += "(Highly fragmented - diverse business ecosystem)\n"
        else:
            response += "(Well-connected - potential systemic risks)\n"

        response += f"- Average Clustering: {stats['average_clustering']:.3f} "
        if stats['average_clustering'] > 0.3:
            response += "(High clustering - tight-knit business groups)\n\n"
        else:
            response += "(Low clustering - independent operations)\n\n"

    # Recommendations
    response += "**Investigative Recommendations:**\n"
    if risk_level == "High":
        response += "- Immediate audit of suspicious entities\n"
        response += "- Cross-agency data verification\n"
        response += "- Enhanced monitoring of circular transaction patterns\n"
    elif risk_level == "Medium":
        response += "- Targeted review of flagged entities\n"
        response += "- Monitor for emerging patterns\n"
    else:
        response += "- Continue routine monitoring\n"
        response += "- Update risk models with new data\n"

    response += "\n**AI Confidence:** Analysis based on graph analytics and statistical thresholds"

    return response