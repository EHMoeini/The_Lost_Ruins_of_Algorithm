from collections import deque


def solve(grid, R, C, sr, sc, er, ec, M):
    
    # position of each treasure
    treasures = []
    for row in range(R):
        for col in range(C):
            if grid[row][col] == 'T':
                treasures.append((row, col))
    
    # assign index to each treasure
    treasure_index = {}
    for idx, (tr, tc) in enumerate(treasures):
        treasure_index[(tr, tc)] = idx
    
    # check whether start position has a treasure
    start_has_treasure = (sr, sc) in treasure_index
    
    # check if start == end
    if sr == er and sc == ec:
        if M == 0:
            # no moves possible
            return 1 if start_has_treasure else 0
        elif M < 0:
            # invalid number of possible moves
            return -1
        
    # if start or end position is blocked
    if grid[sr][sc] == '#' or grid[er][ec] == '#':
        return -1


    
    # initial state
    initial_mask = (1 << treasure_index[(sr, sc)]) if start_has_treasure else 0
    initial_state = (sr, sc, 0, initial_mask)
    
    # BFS with state: (row, col, moves_used, treasure_mask)
    queue = deque()
    queue.append(initial_state)

    visited = set()
    
    # directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    max_treasures = -1
    
    while queue:
        row, col, moves_used, treasure_mask = queue.popleft()

        # check whether it's the end position
        if row == er and col == ec:
            # count treasures from the mask (indices in the binary mask correspond to the relative index of the treasure)
            # for example mask 101 means treasures of index 0 and index 2 are gathered 
            treasures_collected = bin(treasure_mask).count('1')
            max_treasures = max(max_treasures, treasures_collected)
        
        if moves_used == M:
            continue
        
        for dr, dc in directions:
            new_row, new_column = row + dr, col + dc
            
            # check bounds
            if 0 <= new_row < R and 0 <= new_column < C:
                # check wall
                if grid[new_row][new_column] != '#':
                    # calculate new mask
                    new_mask = treasure_mask
                    if (new_row, new_column) in treasure_index:
                        t_idx = treasure_index[(new_row, new_column)]
                        new_mask = treasure_mask | (1 << t_idx)
                    
                    new_moves = moves_used + 1
                    
                    # check if this state is better than what we've seen
                    new_state = (new_row, new_column, new_moves, new_mask)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append(new_state)
    
    return max_treasures


def main():
    # get number of rows and columns
    R, C = map(int, input().split())
    
    # get the grid
    grid = []
    for i in range(R):
        row = input().split()
        grid.append(row)
    
    # get start, end, and move budget
    sr, sc, er, ec, M = map(int, input().split())
    
    result = solve(grid, R, C, sr, sc, er, ec, M)
    print(result)


if __name__ == "__main__":
    main()
