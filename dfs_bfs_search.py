
from collections import deque
from kyiv_metro_graph import create_kyiv_metro_graph


def dfs_path(graph, start, goal, path=None):
    if path is None:
        path = []

    path = path + [start]

    if start == goal:
        return path

    if start not in graph:
        return None

    neighbors = sorted(graph.neighbors(start))

    for neighbor in neighbors:
        if neighbor not in path:
            new_path = dfs_path(graph, neighbor, goal, path)
            if new_path:
                return new_path

    return None


def dfs_path_iterative(graph, start, goal):
    if start not in graph or goal not in graph:
        return None

    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        neighbors = sorted(graph.neighbors(current), reverse=True)
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None


def bfs_path(graph, start, goal):
    if start not in graph or goal not in graph:
        return None

    if start == goal:
        return [start]

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()

        neighbors = sorted(graph.neighbors(current))

        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]

                if neighbor == goal:
                    return new_path

                visited.add(neighbor)
                queue.append((neighbor, new_path))

    return None


def compare_paths(graph, start, goal):
    dfs_result = dfs_path(graph, start, goal)
    bfs_result = bfs_path(graph, start, goal)

    return {
        "start": start,
        "goal": goal,
        "dfs_path": dfs_result,
        "bfs_path": bfs_result,
        "dfs_length": len(dfs_result) if dfs_result else 0,
        "bfs_length": len(bfs_result) if bfs_result else 0,
    }


def print_path_comparison(comparison):
    print(f"\n{'='*70}")
    print(f"МАРШРУТ: {comparison['start']} → {comparison['goal']}")
    print(f"{'='*70}")

    print(f"\n🔵 BFS шлях (Пошук в ширину):")
    print(f"   Довжина: {comparison['bfs_length']} станцій")
    if comparison['bfs_path']:
        print(f"   Маршрут: {' → '.join(comparison['bfs_path'])}")

    print(f"\n🔴 DFS шлях (Пошук в глибину):")
    print(f"   Довжина: {comparison['dfs_length']} станцій")
    if comparison['dfs_path']:
        print(f"   Маршрут: {' → '.join(comparison['dfs_path'])}")

    print(f"\n📊 Аналіз:")
    if comparison['bfs_length'] < comparison['dfs_length']:
        diff = comparison['dfs_length'] - comparison['bfs_length']
        print(f"   • BFS знайшов коротший шлях на {diff} станцій")
        print(f"   • BFS оптимальний для незважених графів (знаходить найкоротший шлях)")
        print(f"   • DFS пішов глибше перед тим, як знайти ціль")
    elif comparison['bfs_length'] > comparison['dfs_length']:
        print(f"   • DFS знайшов коротший шлях (незвично для цієї структури графа)")
    else:
        print(f"   • Обидва алгоритми знайшли шляхи однакової довжини")
        if comparison['bfs_path'] != comparison['dfs_path']:
            print(f"   • Шляхи різні, але однакової довжини")


def main():
    print("Створення графа мережі Київського метро...")
    G = create_kyiv_metro_graph()

    print("\n" + "="*70)
    print("ПОРІВНЯННЯ ПОШУКУ ШЛЯХІВ DFS та BFS")
    print("Транспортна мережа Київського метрополітену")
    print("="*70)

    test_cases = [
        ("Akademmistechko", "Lisova"),
        ("Heroiv Dnipra", "Syrets"),
        ("Khreshchatyk", "Zoloti Vorota"),
        ("Akademmistechko", "Chervonyi Khutir"),
        ("Teremky", "Osokorky"),
    ]

    print("\n" + "-"*70)
    print("ПОЯСНЕННЯ АЛГОРИТМІВ")
    print("-"*70)
    print("""
    DFS (Пошук в глибину - Depth-First Search):
    • Використовує СТЕК (LIFO - останній прийшов, перший вийшов)
    • Досліджує якомога глибше вздовж кожної гілки перед поверненням
    • Може НЕ знайти найкоротший шлях
    • Ефективний по пам'яті для глибоких графів
    • Застосування: розв'язання лабіринтів, топологічне сортування, виявлення циклів

    BFS (Пошук в ширину - Breadth-First Search):
    • Використовує ЧЕРГУ (FIFO - перший прийшов, перший вийшов)
    • Досліджує всіх сусідів на поточній глибині перед переходом глибше
    • ГАРАНТУЄ найкоротший шлях у незважених графах
    • Використовує більше пам'яті (зберігає всі вузли поточного рівня)
    • Застосування: найкоротший шлях, обхід по рівнях, соціальні мережі
    """)

    for start, goal in test_cases:
        comparison = compare_paths(G, start, goal)
        print_path_comparison(comparison)

    print("\n" + "="*70)
    print("ПІДСУМОК ТА ПОЯСНЕННЯ")
    print("="*70)
    print("""
    Чому DFS та BFS знаходять різні шляхи?

    1. ПОРЯДОК ДОСЛІДЖЕННЯ:
       • BFS досліджує рівень за рівнем (спочатку всі станції на відстані 1, потім 2 і т.д.)
       • DFS занурюється глибоко в одну гілку перед спробою альтернатив

    2. ОПТИМАЛЬНІСТЬ ШЛЯХУ:
       • BFS завжди знаходить НАЙКОРОТШИЙ шлях у незважених графах,
         тому що досліджує всі шляхи довжини N перед шляхами довжини N+1
       • DFS може знайти довший шлях, бо рано фіксується на одному напрямку

    3. СПЕЦИФІКА МЕРЕЖІ МЕТРО:
       • Київське метро - лінійна мережа з пересадочними станціями
       • BFS ефективно знаходить шляхи через пересадки, коли це вигідно
       • DFS може пройти всю лінію перед тим, як спробувати пересадку

    4. ПРАКТИЧНІ ВИСНОВКИ:
       • Для пошуку найкоротшого маршруту: використовуйте BFS
       • Для дослідження всіх можливих маршрутів: використовуйте DFS
       • Для зважених графів (час подорожі): використовуйте алгоритм Дейкстри
    """)


if __name__ == "__main__":
    main()
