"""
Problem 3 - "The Mandatory Collection"
Solution using BFS over state (row, col, mask) to find minimum moves
to collect at least K treasures while traveling from S to E.

Algorithm: BFS over state (row, col, mask) where mask is a bitmask of collected treasures
Termination: First time we reach (er, ec) with >= K treasures collected
"""

import sys
from collections import deque


def solve(grid, R, C, sr, sc, er, ec, K):
    """
    Returns the minimum number of moves for any path from (sr, sc) to (er, ec)
    that collects at least K treasures, or -1 if no such path exists.
    
    Args:
        grid: 2D list of strings representing the grid
        R: number of rows
        C: number of columns
        sr, sc: start row and column
        er, ec: end row and column
        K: minimum number of treasures to collect
    
    Returns:
        Minimum number of moves, or -1 if no valid path exists
    """
    
    # Find all treasure positions and index them in reading order
    treasure_positions = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'T':
                treasure_positions.append((r, c))
    
    num_treasures = len(treasure_positions)
    
    # If K > total treasures, impossible
    if K > num_treasures:
        return -1
    
    # Special case: K = 0, just find shortest path from S to E
    if K == 0:
        return bfs_shortest_path(grid, R, C, sr, sc, er, ec)
    
    # Create a mapping from position to treasure index
    treasure_index = {}
    for idx, (tr, tc) in enumerate(treasure_positions):
        treasure_index[(tr, tc)] = idx
    
    # Check if start or end position has a treasure
    start_has_treasure = (sr, sc) in treasure_index
    end_has_treasure = (er, ec) in treasure_index
    
    # BFS over state (row, col, mask)
    # visited[row][col][mask] = True if this state has been visited
    # We use a set for sparse storage
    visited = set()
    
    # Initial state
    initial_mask = (1 << treasure_index[(sr, sc)]) if start_has_treasure else 0
    initial_state = (sr, sc, initial_mask)
    
    # Queue for BFS: (row, col, treasure_mask, moves)
    queue = deque()
    queue.append((sr, sc, initial_mask, 0))
    visited.add(initial_state)
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        r, c, mask, moves = queue.popleft()
        
        # Check if we've reached the end with enough treasures
        treasures_collected = bin(mask).count('1')
        if r == er and c == ec and treasures_collected >= K:
            return moves
        
        # Try all four directions
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < R and 0 <= nc < C:
                # Check if not a wall
                if grid[nr][nc] != '#':
                    # Calculate new mask
                    new_mask = mask
                    if (nr, nc) in treasure_index:
                        t_idx = treasure_index[(nr, nc)]
                        new_mask = mask | (1 << t_idx)
                    
                    # Check if this state has been visited
                    new_state = (nr, nc, new_mask)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((nr, nc, new_mask, moves + 1))
    
    # No valid path found
    return -1


def bfs_shortest_path(grid, R, C, sr, sc, er, ec):
    """
    Standard BFS to find shortest path from (sr, sc) to (er, ec).
    Used when K = 0.
    """
    if sr == er and sc == ec:
        return 0
    
    visited = [[False] * C for _ in range(R)]
    visited[sr][sc] = True
    
    queue = deque([(sr, sc, 0)])  # (row, col, moves)
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        r, c, moves = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < R and 0 <= nc < C:
                if grid[nr][nc] != '#' and not visited[nr][nc]:
                    if nr == er and nc == ec:
                        return moves + 1
                    
                    visited[nr][nc] = True
                    queue.append((nr, nc, moves + 1))
    
    return -1


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
    
    # Parse start, end, and K
    sr, sc, er, ec, K = map(int, input_data[line_idx].split())
    
    # Solve and output
    result = solve(grid, R, C, sr, sc, er, ec, K)
    print(result)


if __name__ == "__main__":
    main()
