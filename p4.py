"""
Problem 4 - "The Rescue Mission"
Solution using Maximum Flow on a node-split graph to find maximum vertex-disjoint paths

Algorithm: Edmonds-Karp max-flow on node-split graph
- Split each cell (r,c) into node_in(r,c) and node_out(r,c)
- Edge from node_in to node_out with capacity 1 (∞ for S and E)
- Grid edges: node_out(u) -> node_in(v) with capacity ∞
- Max flow from node_out(S) to node_in(E) = max vertex-disjoint paths
"""

import sys
from collections import deque


def solve(grid, R, C, sr, sc, er, ec):
    """
    Returns the maximum number of vertex-disjoint paths from (sr, sc) to (er, ec).
    
    Args:
        grid: 2D list of strings representing the grid
        R: number of rows
        C: number of columns
        sr, sc: start row and column
        er, ec: end row and column
    
    Returns:
        Maximum number of vertex-disjoint paths, or 0 if no path exists
    """
    
    # Special case: S == E
    if sr == er and sc == ec:
        return 1
    
    # Check if S and E are passable
    if grid[sr][sc] == '#' or grid[er][ec] == '#':
        return 0
    
    # Node splitting: each cell (r, c) has two nodes
    # node_in(r, c) = (r * C + c) * 2
    # node_out(r, c) = (r * C + c) * 2 + 1
    def node_in(r, c):
        return (r * C + c) * 2
    
    def node_out(r, c):
        return (r * C + c) * 2 + 1
    
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
    for r in range(R):
        for c in range(C):
            if grid[r][c] != '#':
                # Capacity is ∞ for S and E, 1 for intermediate cells
                if (r == sr and c == sc) or (r == er and c == ec):
                    cap = float('inf')
                else:
                    cap = 1
                add_edge(node_in(r, c), node_out(r, c), cap)
    
    # Add grid edges (node_out(u) -> node_in(v)) for adjacent passable cells
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(R):
        for c in range(C):
            if grid[r][c] != '#':
                u_out = node_out(r, c)
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#':
                        v_in = node_in(nr, nc)
                        # Capacity ∞ for grid edges
                        add_edge(u_out, v_in, float('inf'))
    
    # Edmonds-Karp algorithm (BFS-based max flow)
    def bfs_find_path():
        """Find augmenting path using BFS, return path and bottleneck capacity"""
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
    # Read input from stdin
    input_data = sys.stdin.read().split('\n')
    line_idx = 0
    
    # Parse R and C
    R, C = map(int, input_data[line_idx].split())
    line_idx += 1
    
    # Parse grid
    grid = []
    for i in range(R):
        row = input_data[line_idx].split()
        grid.append(row)
        line_idx += 1
    
    # Parse start and end positions
    sr, sc, er, ec = map(int, input_data[line_idx].split())
    
    # Solve and output
    result = solve(grid, R, C, sr, sc, er, ec)
    print(result)


if __name__ == "__main__":
    main()
