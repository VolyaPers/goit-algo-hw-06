"""
Kyiv Metro Transportation Network Graph Analysis

This module creates and analyzes a graph representing the Kyiv Metro system
using NetworkX library. The network includes all three metro lines with
their stations and connections.
"""

import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from collections import Counter


def create_kyiv_metro_graph():
    """
    Create a graph representing the Kyiv Metro transportation network.

    The graph includes:
    - Red Line (M1 - Sviatoshynsko-Brovarska)
    - Blue Line (M2 - Obolon-Teremky)
    - Green Line (M3 - Syretsko-Pecherska)

    Transfer stations are connected across lines.

    Returns:
        nx.Graph: NetworkX graph representing the metro network
    """
    G = nx.Graph()

    # Red Line (M1) - Sviatoshynsko-Brovarska (West to East)
    red_line = [
        "Akademmistechko", "Zhytomyrska", "Sviatoshyn", "Nyvky",
        "Beresteiska", "Shuliavska", "Politekhnichnyi Instytut",
        "Vokzalna", "Universytet", "Teatralna", "Khreshchatyk",
        "Arsenalna", "Dnipro", "Hidropark", "Livoberezhna",
        "Darnytsia", "Chernihivska", "Lisova"
    ]

    # Blue Line (M2) - Obolon-Teremky (North to South)
    blue_line = [
        "Heroiv Dnipra", "Minska", "Obolon", "Pochaina",
        "Tarasa Shevchenka", "Kontraktova Ploshcha", "Poshtova Ploshcha",
        "Maidan Nezalezhnosti", "Ploshcha Ukrainskykh Heroiv",
        "Olimpiiska", "Palats Ukraina", "Lybidska", "Demiivska",
        "Holosiivska", "Vasylkivska", "Vystavkovyi Tsentr", "Ipodrom",
        "Teremky"
    ]

    # Green Line (M3) - Syretsko-Pecherska (Northwest to Southeast)
    green_line = [
        "Syrets", "Dorohozhychi", "Lukianivska", "Zoloti Vorota",
        "Palats Sportu", "Klovska", "Pecherska", "Druzhby Narodiv",
        "Vydubychi", "Slavutych", "Osokorky", "Pozniaky",
        "Kharkivska", "Vyrlytsia", "Boryspilska", "Chervonyi Khutir"
    ]

    # Add edges for Red Line with line attribute
    for i in range(len(red_line) - 1):
        G.add_edge(red_line[i], red_line[i + 1], line="red", weight=1)

    # Add edges for Blue Line
    for i in range(len(blue_line) - 1):
        G.add_edge(blue_line[i], blue_line[i + 1], line="blue", weight=1)

    # Add edges for Green Line
    for i in range(len(green_line) - 1):
        G.add_edge(green_line[i], green_line[i + 1], line="green", weight=1)

    # Add transfer connections (interchange stations)
    # Teatralna (Red) <-> Zoloti Vorota (Green)
    G.add_edge("Teatralna", "Zoloti Vorota", line="transfer", weight=0.5)

    # Khreshchatyk (Red) <-> Maidan Nezalezhnosti (Blue)
    G.add_edge("Khreshchatyk", "Maidan Nezalezhnosti", line="transfer", weight=0.5)

    # Palats Sportu (Green) <-> Ploshcha Ukrainskykh Heroiv (Blue)
    G.add_edge("Palats Sportu", "Ploshcha Ukrainskykh Heroiv", line="transfer", weight=0.5)

    # Add line information to nodes
    for station in red_line:
        if station in G.nodes:
            G.nodes[station]["line"] = G.nodes[station].get("line", []) + ["red"]

    for station in blue_line:
        if station in G.nodes:
            G.nodes[station]["line"] = G.nodes[station].get("line", []) + ["blue"]

    for station in green_line:
        if station in G.nodes:
            G.nodes[station]["line"] = G.nodes[station].get("line", []) + ["green"]

    return G


def analyze_graph(G):
    """
    Analyze and print main characteristics of the graph.

    Args:
        G: NetworkX graph to analyze
    """
    print("=" * 60)
    print("KYIV METRO NETWORK ANALYSIS")
    print("=" * 60)

    # Basic characteristics
    print("\n1. BASIC CHARACTERISTICS")
    print("-" * 40)
    print(f"   Number of vertices (stations): {G.number_of_nodes()}")
    print(f"   Number of edges (connections): {G.number_of_edges()}")

    # Density
    density = nx.density(G)
    print(f"   Graph density: {density:.4f}")

    # Check connectivity
    is_connected = nx.is_connected(G)
    print(f"   Is connected: {is_connected}")

    if is_connected:
        # Diameter (longest shortest path)
        diameter = nx.diameter(G)
        print(f"   Diameter (longest shortest path): {diameter}")

        # Average shortest path length
        avg_path = nx.average_shortest_path_length(G)
        print(f"   Average shortest path length: {avg_path:.2f}")

    # Degree analysis
    print("\n2. DEGREE ANALYSIS")
    print("-" * 40)
    degrees = dict(G.degree())
    degree_values = list(degrees.values())

    print(f"   Average degree: {sum(degree_values) / len(degree_values):.2f}")
    print(f"   Minimum degree: {min(degree_values)}")
    print(f"   Maximum degree: {max(degree_values)}")

    # Degree distribution
    degree_count = Counter(degree_values)
    print("\n   Degree distribution:")
    for degree in sorted(degree_count.keys()):
        count = degree_count[degree]
        print(f"      Degree {degree}: {count} station(s)")

    # Stations with highest degree (transfer stations)
    print("\n3. TRANSFER STATIONS (highest connectivity)")
    print("-" * 40)
    sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    for station, degree in sorted_degrees[:6]:
        if degree > 2:
            print(f"   {station}: degree {degree}")

    # Centrality measures
    print("\n4. CENTRALITY ANALYSIS")
    print("-" * 40)

    # Betweenness centrality
    betweenness = nx.betweenness_centrality(G)
    top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
    print("   Top 5 stations by betweenness centrality:")
    for station, value in top_betweenness:
        print(f"      {station}: {value:.4f}")

    # Closeness centrality
    closeness = nx.closeness_centrality(G)
    top_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\n   Top 5 stations by closeness centrality:")
    for station, value in top_closeness:
        print(f"      {station}: {value:.4f}")

    # Clustering coefficient
    print("\n5. CLUSTERING")
    print("-" * 40)
    avg_clustering = nx.average_clustering(G)
    print(f"   Average clustering coefficient: {avg_clustering:.4f}")

    # Line statistics
    print("\n6. LINE STATISTICS")
    print("-" * 40)
    edge_lines = [G[u][v].get("line", "unknown") for u, v in G.edges()]
    line_counts = Counter(edge_lines)
    for line, count in line_counts.items():
        print(f"   {line.capitalize()} line edges: {count}")

    print("\n" + "=" * 60)


def visualize_graph(G):
    """
    Visualize the Kyiv Metro network graph.

    Args:
        G: NetworkX graph to visualize
    """
    plt.figure(figsize=(16, 12))

    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # Color edges by line
    edge_colors = []
    for u, v in G.edges():
        line = G[u][v].get("line", "gray")
        if line == "red":
            edge_colors.append("#E63946")
        elif line == "blue":
            edge_colors.append("#457B9D")
        elif line == "green":
            edge_colors.append("#2A9D8F")
        elif line == "transfer":
            edge_colors.append("#F4A261")
        else:
            edge_colors.append("gray")

    # Color nodes based on degree (transfer stations highlighted)
    degrees = dict(G.degree())
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if degrees[node] > 2:
            node_colors.append("#E9C46A")  # Transfer station
            node_sizes.append(800)
        else:
            node_colors.append("#A8DADC")  # Regular station
            node_sizes.append(400)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2.5, alpha=0.8)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes,
                           edgecolors="black", linewidths=1.5)

    # Draw labels with smaller font
    nx.draw_networkx_labels(G, pos, font_size=7, font_weight="bold")

    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], color="#E63946", linewidth=3, label="Red Line (M1)"),
        plt.Line2D([0], [0], color="#457B9D", linewidth=3, label="Blue Line (M2)"),
        plt.Line2D([0], [0], color="#2A9D8F", linewidth=3, label="Green Line (M3)"),
        plt.Line2D([0], [0], color="#F4A261", linewidth=3, linestyle="--", label="Transfer"),
        plt.scatter([0], [0], c="#E9C46A", s=100, edgecolors="black", label="Transfer Station"),
        plt.scatter([0], [0], c="#A8DADC", s=60, edgecolors="black", label="Regular Station"),
    ]
    plt.legend(handles=legend_elements, loc="upper left", fontsize=10)

    plt.title("Kyiv Metro Transportation Network", fontsize=16, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("kyiv_metro_graph.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("\nGraph visualization saved to 'kyiv_metro_graph.png'")


def main():
    """Main function to create, analyze, and visualize the metro graph."""
    # Create the graph
    print("Creating Kyiv Metro network graph...")
    G = create_kyiv_metro_graph()

    # Analyze the graph
    analyze_graph(G)

    # Visualize the graph
    print("\nGenerating visualization...")
    visualize_graph(G)


if __name__ == "__main__":
    main()
