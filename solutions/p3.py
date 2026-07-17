from collections import deque


def solve(grid, R, C, sr, sc, er, ec, K):
    
    # find all treasure positions and assign index
    treasure_positions = []
    for row in range(R):
        for col in range(C):
            if grid[row][col] == 'T':
                treasure_positions.append((row, col))
    
    num_treasures = len(treasure_positions)
    
    # if K > total treasures, impossible
    if K > num_treasures:
        return -1
    
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
        row, col, mask = queue.popleft()
        
        current_moves = moves[(row,col,mask)]

        # check if we've reached the end with enough treasures
        treasures_collected = bin(mask).count('1')
        if row == er and col == ec and treasures_collected >= K:
            return current_moves
        
        # visit neighbors
        for dr, dc in directions:
            neighbor_row, neighbor_col = row + dr, col + dc
            
            if 0 <= neighbor_row < R and 0 <= neighbor_col < C:
                if grid[neighbor_row][neighbor_col] != '#':
                    # calculate new mask
                    new_mask = mask
                    if (neighbor_row, neighbor_col) in treasure_index:
                        t_idx = treasure_index[(neighbor_row, neighbor_col)]
                        new_mask = mask | (1 << t_idx)
                    
                    # check if this state has been visited
                    new_state = (neighbor_row, neighbor_col, new_mask)
                    if new_state not in moves:
                        moves[new_state] = current_moves + 1
                        queue.append(new_state)
    
    return -1


def main():
    # get number of rows and columns
    R, C = map(int, input().split())
    
    # get the grid
    grid = []
    for i in range(R):
        row = input().split()
        grid.append(row)
    
    sr, sc, er, ec, K = map(int, input().split())
    
    result = solve(grid, R, C, sr, sc, er, ec, K)
    print(result)


if __name__ == "__main__":
    main()
