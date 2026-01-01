import heapq
import networkx as nx
from kyiv_metro_graph import create_kyiv_metro_graph


def add_travel_times(G):
    G_weighted = G.copy()

    for u, v, data in G_weighted.edges(data=True):
        line = data.get('line', 'unknown')

        if line == 'transfer':
            G_weighted[u][v]['weight'] = 5
        else:
            base_time = 2.5
            variation = ((hash(u) + hash(v)) % 10) / 10
            G_weighted[u][v]['weight'] = round(base_time + variation, 1)

    return G_weighted


def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start] = 0

    previous = {node: None for node in graph.nodes()}

    priority_queue = [(0, start)]

    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue

            weight = graph[current_node][neighbor].get('weight', 1)
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous


def reconstruct_path(previous, start, end):
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    if path and path[0] == start:
        return path
    return []


def find_all_shortest_paths(graph):
    all_paths = {}
    nodes = list(graph.nodes())

    for source in nodes:
        distances, previous = dijkstra(graph, source)

        for target in nodes:
            if source != target:
                path = reconstruct_path(previous, source, target)
                all_paths[(source, target)] = {
                    'distance': distances[target],
                    'path': path
                }

    return all_paths


def print_shortest_paths_summary(graph, all_paths):
    nodes = list(graph.nodes())
    n = len(nodes)

    print("=" * 70)
    print("АНАЛІЗ НАЙКОРОТШИХ ШЛЯХІВ (АЛГОРИТМ ДЕЙКСТРИ)")
    print("Транспортна мережа Київського метрополітену")
    print("=" * 70)

    distances = [p['distance'] for p in all_paths.values()]
    avg_distance = sum(distances) / len(distances)
    max_distance = max(distances)
    min_distance = min(distances)

    longest_path_key = max(all_paths, key=lambda k: all_paths[k]['distance'])
    shortest_path_key = min(all_paths, key=lambda k: all_paths[k]['distance'])

    print(f"\n📊 ЗАГАЛЬНА СТАТИСТИКА")
    print("-" * 50)
    print(f"   Кількість станцій: {n}")
    print(f"   Кількість пар станцій: {n * (n - 1)}")
    print(f"   Середній час подорожі: {avg_distance:.1f} хв")
    print(f"   Мінімальний час: {min_distance:.1f} хв")
    print(f"   Максимальний час: {max_distance:.1f} хв")

    print(f"\n🚇 НАЙДОВША ПОДОРОЖ")
    print("-" * 50)
    longest = all_paths[longest_path_key]
    print(f"   Маршрут: {longest_path_key[0]} → {longest_path_key[1]}")
    print(f"   Час: {longest['distance']:.1f} хв")
    print(f"   Кількість станцій: {len(longest['path'])}")
    print(f"   Шлях: {' → '.join(longest['path'][:5])}...")

    print(f"\n🚀 НАЙКОРОТША ПОДОРОЖ")
    print("-" * 50)
    shortest = all_paths[shortest_path_key]
    print(f"   Маршрут: {shortest_path_key[0]} → {shortest_path_key[1]}")
    print(f"   Час: {shortest['distance']:.1f} хв")
    print(f"   Шлях: {' → '.join(shortest['path'])}")


def print_example_paths(graph, all_paths):

    example_routes = [
        ("Akademmistechko", "Lisova"),
        ("Heroiv Dnipra", "Chervonyi Khutir"),
        ("Khreshchatyk", "Zoloti Vorota"),
        ("Teremky", "Syrets"),
        ("Obolon", "Vydubychi"),
    ]

    print(f"\n{'=' * 70}")
    print("ПРИКЛАДИ НАЙКОРОТШИХ ШЛЯХІВ")
    print("=" * 70)

    for start, end in example_routes:
        if (start, end) in all_paths:
            path_info = all_paths[(start, end)]
            path = path_info['path']
            distance = path_info['distance']

            print(f"\n📍 {start} → {end}")
            print("-" * 50)
            print(f"   ⏱️  Час подорожі: {distance:.1f} хв")
            print(f"   🚉 Кількість станцій: {len(path)}")
            print(f"   📋 Маршрут:")

            for i, station in enumerate(path):
                if i == 0:
                    print(f"      🚩 {station} (старт)")
                elif i == len(path) - 1:
                    print(f"      🏁 {station} (фініш)")
                else:
                    if graph.degree(station) > 2:
                        print(f"      🔄 {station} (пересадка)")
                    else:
                        print(f"      ○  {station}")


def print_distance_matrix_sample(graph, all_paths):

    important_stations = [
        "Akademmistechko", "Khreshchatyk", "Lisova",
        "Heroiv Dnipra", "Teremky", "Syrets", "Chervonyi Khutir"
    ]

    print(f"\n{'=' * 70}")
    print("МАТРИЦЯ ВІДСТАНЕЙ (вибрані станції, хв)")
    print("=" * 70)

    short_names = {
        "Akademmistechko": "Акад",
        "Khreshchatyk": "Хрещ",
        "Lisova": "Лісо",
        "Heroiv Dnipra": "ГерД",
        "Teremky": "Терм",
        "Syrets": "Сирц",
        "Chervonyi Khutir": "ЧерХ"
    }

    print(f"\n{'':12}", end="")
    for station in important_stations:
        print(f"{short_names[station]:>6}", end="")
    print()

    print("-" * (12 + 6 * len(important_stations)))

    for source in important_stations:
        print(f"{short_names[source]:12}", end="")
        for target in important_stations:
            if source == target:
                print(f"{'--':>6}", end="")
            else:
                dist = all_paths[(source, target)]['distance']
                print(f"{dist:>6.1f}", end="")
        print()


def compare_with_networkx(graph, start, end):

    distances, previous = dijkstra(graph, start)
    our_path = reconstruct_path(previous, start, end)
    our_distance = distances[end]

    nx_path = nx.dijkstra_path(graph, start, end, weight='weight')
    nx_distance = nx.dijkstra_path_length(graph, start, end, weight='weight')

    print(f"\n{'=' * 70}")
    print("ПЕРЕВІРКА: ПОРІВНЯННЯ З NETWORKX")
    print("=" * 70)
    print(f"\nМаршрут: {start} → {end}")
    print(f"\n   Наша реалізація:")
    print(f"      Відстань: {our_distance:.1f} хв")
    print(f"      Шлях: {len(our_path)} станцій")
    print(f"\n   NetworkX реалізація:")
    print(f"      Відстань: {nx_distance:.1f} хв")
    print(f"      Шлях: {len(nx_path)} станцій")
    print(f"\n   ✅ Результати {'збігаються' if abs(our_distance - nx_distance) < 0.01 else 'НЕ збігаються'}!")


def main():

    print("Створення графа мережі Київського метро...")
    G = create_kyiv_metro_graph()

    print("Додавання ваг (час подорожі) до ребер...")
    G_weighted = add_travel_times(G)

    print(f"\n📊 ВАГИ РЕБЕР (час подорожі)")
    print("-" * 50)
    print("   Між сусідніми станціями: 2.5-3.4 хв")
    print("   Пересадка між лініями: 5.0 хв")

    print("\nОбчислення найкоротших шляхів між усіма парами станцій...")
    all_paths = find_all_shortest_paths(G_weighted)

    print_shortest_paths_summary(G_weighted, all_paths)
    print_example_paths(G_weighted, all_paths)
    print_distance_matrix_sample(G_weighted, all_paths)

    compare_with_networkx(G_weighted, "Akademmistechko", "Chervonyi Khutir")

    print(f"\n{'=' * 70}")
    print("ВИСНОВКИ")
    print("=" * 70)
    print("""
    Алгоритм Дейкстри:

    1. ПРИЗНАЧЕННЯ:
       • Знаходить найкоротші шляхи у зважених графах
       • Працює з невід'ємними вагами ребер
       • Оптимальний для транспортних мереж з різним часом подорожі

    2. СКЛАДНІСТЬ:
       • Часова: O((V + E) log V) з бінарною купою
       • Просторова: O(V) для зберігання відстаней

    3. ПЕРЕВАГА НАД BFS:
       • BFS знаходить найкоротший шлях за кількістю ребер
       • Дейкстра знаходить найкоротший шлях за сумою ваг
       • У метро: враховує різний час між станціями та пересадки

    4. ПРАКТИЧНЕ ЗАСТОСУВАННЯ:
       • GPS-навігація
       • Маршрутизація в мережах
       • Транспортне планування
       • Логістика та доставка
    """)


if __name__ == "__main__":
    main()
