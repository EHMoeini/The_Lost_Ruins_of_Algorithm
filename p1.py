"""
Problem 1 - "The Time-Limited Expedition"
Solution using BFS with state space (row, col, moves_used, treasure_mask)

Algorithm: BFS/DP over a 4-dimensional state space
State: (row, col, moves_used, mask) where mask is a bitmask of collected treasures
"""

import sys
from collections import deque


def solve(grid, R, C, sr, sc, er, ec, M):
    """
    Returns the maximum number of treasures collectible on any path from (sr, sc) 
    to (er, ec) using at most M moves, or -1 if no such path exists.
    
    Args:
        grid: 2D list of strings representing the grid
        R: number of rows
        C: number of columns
        sr, sc: start row and column
        er, ec: end row and column
        M: maximum number of moves allowed
    
    Returns:
        Maximum number of treasures collectible, or -1 if no valid path exists
    """
    
    # position of each treasure
    treasures = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'T':
                treasures.append((r, c))
    
    num_treasures = len(treasures)
    
    # assign index to each treasure
    treasure_index = {}
    for idx, (tr, tc) in enumerate(treasures):
        treasure_index[(tr, tc)] = idx
    
    # check whether start or end position has a treasure
    start_has_treasure = (sr, sc) in treasure_index
    end_has_treasure = (er, ec) in treasure_index
    
    # check if start == end
    if sr == er and sc == ec:
        if M == 0:
            # Can't move, only1 collect treasure at S if it exists
            return 1 if start_has_treasure else 0
        elif M < 0:
            # Invalid move budget
            return -1
    
    # BFS with state: (row, col, moves_used, treasure_mask)
    # We want to minimize moves_used for each (row, col, mask) state
    # dp[row][col][mask] = minimum moves to reach this state
    
    # Initialize DP table with infinity
    # Using a dictionary for sparse storage
    INF = float('inf')
    dp = {}
    
    # Initial state
    initial_mask = (1 << treasure_index[(sr, sc)]) if start_has_treasure else 0
    initial_state = (sr, sc, 0, initial_mask)
    
    # Queue for BFS: (row, col, moves_used, treasure_mask)
    queue = deque()
    queue.append((sr, sc, 0, initial_mask))
    dp[(sr, sc, initial_mask)] = 0
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    max_treasures = -1
    
    while queue:
        r, c, moves, mask = queue.popleft()
        
        # Check if we've reached the end
        if r == er and c == ec:
            # Count treasures in mask
            treasures_collected = bin(mask).count('1')
            max_treasures = max(max_treasures, treasures_collected)
            # Don't return immediately - there might be better paths
            continue
        
        # If we've used all moves, can't continue
        if moves >= M:
            continue
        
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
                    
                    new_moves = moves + 1
                    
                    # Check if this state is better than what we've seen
                    state_key = (nr, nc, new_mask)
                    if state_key not in dp or dp[state_key] > new_moves:
                        dp[state_key] = new_moves
                        queue.append((nr, nc, new_moves, new_mask))
    
    return max_treasures


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
    
    # Parse start, end, and move budget
    sr, sc, er, ec, M = map(int, input_data[line_idx].split())
    
    # Solve and output
    result = solve(grid, R, C, sr, sc, er, ec, M)
    print(result)


if __name__ == "__main__":
    main()
