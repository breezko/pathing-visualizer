from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    grid = data.get("grid")
    start = tuple(data.get("start"))
    end = tuple(data.get("end"))
    algorithm = data.get("algorithm", "a*")

    if algorithm == "a*":
        path, expanded = a_star(grid, start, end)
    elif algorithm == "dijkstra":
        path, expanded = dijkstra(grid, start, end)
    elif algorithm == "bfs":
        path, expanded = bfs(grid, start, end)
    elif algorithm == "dfs":
        path, expanded = dfs(grid, start, end)
    elif algorithm == "lee":
        path, expanded = lee(grid, start, end)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    return jsonify({
        "path": path,
        "expanded": expanded
    })

def a_star(grid, start, end):
    """
    A* returning:
    - the final path
    - the list of nodes expanded in order
    """
    from heapq import heappush, heappop

    rows, cols = len(grid), len(grid[0])
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    closed_set = set()

    expanded_nodes = []

    def heuristic(a, b):
        #return 0
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while open_set:
        f_current, current = heappop(open_set)

        if current in closed_set:
            continue

        expanded_nodes.append(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, expanded_nodes

        closed_set.add(current)

        for d in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr = current[0]+d[0]
            nc = current[1]+d[1]
            neighbor = (nr, nc)

            if (
                0 <= nr < rows and
                0 <= nc < cols and
                grid[nr][nc] == 0
            ):
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heappush(open_set, (f_score, neighbor))

    return [], expanded_nodes

def dijkstra(grid, start, end):
    """
    Dijkstra's algorithm returning:
    - the final path
    - the list of nodes expanded in order
    """
    from heapq import heappush, heappop

    rows, cols = len(grid), len(grid[0])
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    closed_set = set()

    expanded_nodes = []

    while open_set:
        g_current, current = heappop(open_set)

        if current in closed_set:
            continue

        expanded_nodes.append(current)

        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, expanded_nodes

        closed_set.add(current)

        for d in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr = current[0] + d[0]
            nc = current[1] + d[1]
            neighbor = (nr, nc)

            if (
                0 <= nr < rows and
                0 <= nc < cols and
                grid[nr][nc] == 0
            ):
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g  # No heuristic
                    heappush(open_set, (f_score, neighbor))

    # No path found
    return [], expanded_nodes

def bfs(grid, start, end):
    """
    BFS algorithm returning:
    - the final path
    - the list of nodes expanded in order
    """
    from collections import deque

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    queue.append(start)
    came_from = {}
    visited = set()
    visited.add(start)

    expanded_nodes = []

    while queue:
        current = queue.popleft()
        expanded_nodes.append(current)

        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, expanded_nodes

        for d in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr = current[0] + d[0]
            nc = current[1] + d[1]
            neighbor = (nr, nc)

            if (
                0 <= nr < rows and
                0 <= nc < cols and
                grid[nr][nc] == 0 and
                neighbor not in visited
            ):
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    # No path found
    return [], expanded_nodes

def dfs(grid, start, end):
    """
    DFS algorithm returning:
    - the final path (not guaranteed to be shortest)
    - the list of nodes expanded in order
    """
    rows, cols = len(grid), len(grid[0])
    stack = []
    stack.append(start)
    came_from = {}
    visited = set()
    visited.add(start)

    expanded_nodes = []

    while stack:
        current = stack.pop()
        expanded_nodes.append(current)

        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, expanded_nodes

        for d in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr = current[0] + d[0]
            nc = current[1] + d[1]
            neighbor = (nr, nc)

            if (
                0 <= nr < rows and
                0 <= nc < cols and
                grid[nr][nc] == 0 and
                neighbor not in visited
            ):
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)

    # No path found
    return [], expanded_nodes

def lee(grid, start, end):
    """
    Lee Algorithm returning:
    - the final shortest path
    - the list of nodes expanded in order
    """
    from collections import deque

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    queue.append(start)

    # Matrix to store wave numbers
    distance = [[-1 for _ in range(cols)] for _ in range(rows)]
    distance[start[0]][start[1]] = 0

    came_from = {}
    expanded_nodes = []
    found = False

    while queue:
        current = queue.popleft()
        expanded_nodes.append(current)

        if current == end:
            found = True
            break

        for d in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr = current[0] + d[0]
            nc = current[1] + d[1]
            neighbor = (nr, nc)

            if (
                0 <= nr < rows and
                0 <= nc < cols and
                grid[nr][nc] == 0 and
                distance[nr][nc] == -1
            ):
                distance[nr][nc] = distance[current[0]][current[1]] + 1
                came_from[neighbor] = current
                queue.append(neighbor)

    if not found:
        return [], expanded_nodes

    # Reconstruct path
    path = []
    current = end
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path, expanded_nodes


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
