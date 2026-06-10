from collections import deque


def solve(grid, R, C, sr, sc, er, ec, K):
    
    # find all treasure positions and index them in reading order
    treasure_positions = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'T':
                treasure_positions.append((r, c))
    
    num_treasures = len(treasure_positions)
    
    # if K > total treasures, impossible
    if K > num_treasures:
        return -1
    
    # if K = 0, just find shortest path from S to E
    if K == 0:
        return bfs_shortest_path(grid, R, C, sr, sc, er, ec)
    
    treasure_index = {}
    for idx, (tr, tc) in enumerate(treasure_positions):
        treasure_index[(tr, tc)] = idx
    
    start_has_treasure = (sr, sc) in treasure_index
    
    initial_mask = (1 << treasure_index[(sr, sc)]) if start_has_treasure else 0
    initial_state = (sr, sc, initial_mask)

    # dictionary to store visited states among number of moves
    moves = {initial_state: 0}
    
    # queue for BFS: (row, col, treasure_mask)
    queue = deque()
    queue.append(initial_state)
    
    # directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        r, c, mask = queue.popleft()
        
        current_moves = moves[(r,c,mask)]

        # check if we've reached the end with enough treasures
        treasures_collected = bin(mask).count('1')
        if r == er and c == ec and treasures_collected >= K:
            return current_moves
        
        # visit neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < R and 0 <= nc < C:
                if grid[nr][nc] != '#':
                    # calculate new mask
                    new_mask = mask
                    if (nr, nc) in treasure_index:
                        t_idx = treasure_index[(nr, nc)]
                        new_mask = mask | (1 << t_idx)
                    
                    # check if this state has been visited
                    new_state = (nr, nc, new_mask)
                    if new_state not in moves:
                        moves[new_state] = current_moves + 1
                        queue.append(new_state)
    
    return -1


def bfs_shortest_path(grid, R, C, sr, sc, er, ec):
    if sr == er and sc == ec:
        return 0
    
    visited = [[False] * C for _ in range(R)]
    visited[sr][sc] = True
    
    queue = deque([(sr, sc, 0)])
    
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
    # get number of rows and columns
    R, C = map(int, input().split())
    
    # get the grid
    grid = []
    for i in range(R):
        row = input().split()
        grid.append(row)
    
    # Parse start, end, and K
    sr, sc, er, ec, K = map(int, input().split())
    
    # Solve and output
    result = solve(grid, R, C, sr, sc, er, ec, K)
    print(result)


if __name__ == "__main__":
    main()
