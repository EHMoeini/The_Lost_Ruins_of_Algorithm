from collections import deque


def solve(grid, R, C, sr, sc, er, ec):
    # Special case: S == E
    if sr == er and sc == ec:
        return 1
    
    # Check if S and E are passable
    if grid[sr][sc] == '#' or grid[er][ec] == '#':
        return 0
    
    # Node splitting: each cell (r, c) has two nodes
    def node_in(row, col):
        return (row * C + col) * 2
    
    def node_out(row, col):
        return (row * C + col) * 2 + 1
    
    # Total nodes: R * C * 2
    total_nodes = R * C * 2
    source = node_out(sr, sc)
    sink = node_in(er, ec)
    
    # Build adjacency list for flow network
    # Each edge: (to, capacity, reverse_edge_index)
    graph = [[] for _ in range(total_nodes)]
    
    def add_edge(u, v, cap):
        # Forward edge with capacity
        graph[u].append([v, cap, len(graph[v])])
        # Reverse edge with 0 capacity
        graph[v].append([u, 0, len(graph[u]) - 1])
    
    # Add internal edges (node_in -> node_out) for each passable cell
    for row in range(R):
        for col in range(C):
            if grid[row][col] != '#':
                # Capacity is ∞ for S and E, 1 for intermediate cells
                if (row == sr and col == sc) or (row == er and col == ec):
                    cap = float('inf')
                else:
                    cap = 1
                add_edge(node_in(row, col), node_out(row, col), cap)
    
    # Add grid edges (node_out(u) -> node_in(v)) for adjacent passable cells
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for row in range(R):
        for col in range(C):
            if grid[row][col] != '#':
                u_out = node_out(row, col)
                for dr, dc in directions:
                    neighbor_row, neighbor_col = row + dr, col + dc
                    if 0 <= neighbor_row < R and 0 <= neighbor_col < C and grid[neighbor_row][neighbor_col] != '#':
                        v_in = node_in(neighbor_row, neighbor_col)
                        # Capacity ∞ for grid edges
                        add_edge(u_out, v_in, float('inf'))
    
    # Edmonds-Karp algorithm
    def bfs_find_path():
        parent = [-1] * total_nodes
        edge_from = [-1] * total_nodes
        visited = [False] * total_nodes
        
        queue = deque([source])
        visited[source] = True
        
        while queue:
            u = queue.popleft()
            
            for idx, (v, cap, rev_idx) in enumerate(graph[u]):
                if not visited[v] and cap > 0:
                    visited[v] = True
                    parent[v] = u
                    edge_from[v] = idx
                    
                    if v == sink:
                        # Reconstruct path and find bottleneck
                        path = []
                        bottleneck = float('inf')
                        curr = sink
                        while curr != source:
                            p = parent[curr]
                            e_idx = edge_from[curr]
                            cap = graph[p][e_idx][1]
                            bottleneck = min(bottleneck, cap)
                            path.append((p, e_idx))
                            curr = p
                        return path, bottleneck
            
                    queue.append(v)
        
        return None, 0
    
    # Compute max flow
    max_flow = 0
    
    while True:
        path, bottleneck = bfs_find_path()
        if path is None or bottleneck == 0:
            break
        
        # Augment flow along path
        for u, e_idx in path:
            # Reduce forward edge capacity
            v, cap, rev_idx = graph[u][e_idx]
            graph[u][e_idx][1] -= bottleneck
            
            # Increase reverse edge capacity
            rev_v, rev_cap, rev_rev_idx = graph[v][rev_idx]
            graph[v][rev_idx][1] += bottleneck
        
        max_flow += bottleneck
    
    return max_flow


def main():
    # get number of rows and columns
    R, C = map(int, input().split())
    
    # get the grid
    grid = []
    for i in range(R):
        row = input().split()
        grid.append(row)
    
    sr, sc, er, ec = map(int, input().split())
    
    # Solve and output
    result = solve(grid, R, C, sr, sc, er, ec)
    print(result)


if __name__ == "__main__":
    main()
