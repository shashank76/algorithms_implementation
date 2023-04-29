import math

# function to compute the Euclidean distance between two vertices
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# function to compute the 2-approximation for METRIC-TSP
def tsp_approx(vertices):
    # Find the shortest edge from each node to another node
    min_edges = {i: (None, float('inf')) for i in range(len(vertices))}
    for i, a in enumerate(vertices):
        for j, b in enumerate(vertices):
            if i == j:
                continue
            d = distance(a, b)
            if d < min_edges[i][1]:
                min_edges[i] = (j, d)

    # Starting from an arbitrary node, follow the shortest edges to form a path
    path = []
    visited = set()
    start = 0
    while len(path) < len(vertices):
        visited.add(start)
        path.append(start)
        next_node, _ = min_edges[start]
        min_edges[start] = (None, float('inf'))
        if next_node is not None and next_node not in visited:
            start = next_node
        else:
            # If we've visited all the neighbors of the current node, pick an non-visited node as the next start
            for i in range(len(vertices)):
                if i not in visited:
                    start = i
                    break

    # Add the final edge to complete the path
    path.append(path[0])

    # Compute the length of the path
    length = sum(distance(vertices[path[i]], vertices[path[i+1]]) for i in range(len(vertices)))

    # Return the path and its length
    return path, length

if __name__ == '__main__':
    vertices = [(0, 0), (3, 0), (1, 1), (2, 2), (1, 3), (3, 3), (4, 4), (5, 4), (6, 3), (5, 2), (6, 1), (5, 0)]
    path, length = tsp_approx(vertices)
    print("path:", path)
    print("Length:", length)