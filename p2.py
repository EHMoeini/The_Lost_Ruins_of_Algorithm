"""
Problem 2 - "Mapping the Ruins"
Solution using BFS from every passable cell to compute average shortest distance

Algorithm: Run BFS from every passable cell, accumulate sum of distances and count of valid pairs
"""

import sys
from collections import deque


def bfs_from_cell(grid, R, C, start_r, start_c):
    """
    Run BFS from a starting cell and return sum of distances to all reachable cells
    and count of reachable cells (excluding self).
    
    Args:
        grid: 2D list of strings
        R: number of rows
        C: number of columns
        start_r, start_c: starting position
    
    Returns:
        Tuple of (sum_of_distances, count_of_reachable_cells)
    """
    # Distance matrix initialized to -1 (unvisited)
    dist = [[-1] * C for _ in range(R)]
    dist[start_r][start_c] = 0
    
    queue = deque([(start_r, start_c)])
    
    total_distance = 0
    reachable_count = 0
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        r, c = queue.popleft()
        current_dist = dist[r][c]
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < R and 0 <= nc < C:
                # Check if passable and unvisited
                if grid[nr][nc] != '#' and dist[nr][nc] == -1:
                    dist[nr][nc] = current_dist + 1
                    total_distance += dist[nr][nc]
                    reachable_count += 1
                    queue.append((nr, nc))
    
    return total_distance, reachable_count


def solve(grid, R, C):
    """
    Returns the average shortest distance over all ordered pairs of passable cells.
    Returns "0.00" if no valid pair exists.
    
    Args:
        grid: 2D list of strings representing the grid
        R: number of rows
        C: number of columns
    
    Returns:
        String representing average distance truncated to 2 decimal places
    """
    # Find all passable cells
    passable_cells = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] != '#':
                passable_cells.append((r, c))
    
    # If less than 2 passable cells, no valid pairs
    if len(passable_cells) < 2:
        return "0.00"
    
    # Run BFS from each passable cell
    total_sum = 0
    total_count = 0
    
    for start_r, start_c in passable_cells:
        dist_sum, count = bfs_from_cell(grid, R, C, start_r, start_c)
        total_sum += dist_sum
        total_count += count
    
    # If no valid pairs exist
    if total_count == 0:
        return "0.00"
    
    # Calculate average and truncate to 2 decimal places
    average = total_sum / total_count
    
    # Truncate without rounding: floor(average * 100) / 100
    import math
    truncated = math.floor(average * 100) / 100
    
    # Format to exactly 2 decimal places
    return f"{truncated:.2f}"


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
    
    # Solve and output
    result = solve(grid, R, C)
    print(result)


if __name__ == "__main__":
    main()
