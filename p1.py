from collections import deque


def solve(grid, R, C, sr, sc, er, ec, M):
    
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
            # no moves possible
            return 1 if start_has_treasure else 0
        elif M < 0:
            # invalid number of possible moves
            return -1
        
    # if start or end position is blocked
    if grid[sr][sc] == '#' or grid[er][ec] == '#':
        return -1


    # BFS with state: (row, col, moves_used, treasure_mask)
    # dp[row][col][mask] = minimum moves to reach this state
    dp = {}
    
    # initial state
    initial_mask = (1 << treasure_index[(sr, sc)]) if start_has_treasure else 0
    initial_state = (sr, sc, 0, initial_mask)
    
    queue = deque()
    queue.append((sr, sc, 0, initial_mask))
    dp[(sr, sc, initial_mask)] = 0
    
    # directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    max_treasures = -1
    
    while queue:
        r, c, moves, mask = queue.popleft()
        
        # check whether it's the end position
        if r == er and c == ec:
            # count treasures from the mask (indices in the binary mask correspond to the relative index of the treasure)
            # for example mask 101 means treasures of index 0 and index 2 are gathered 
            treasures_collected = bin(mask).count('1')
            max_treasures = max(max_treasures, treasures_collected)
        
        if moves == M:
            continue
        
        for dr, dc in directions:
            new_row, new_column = r + dr, c + dc
            
            # check bounds
            if 0 <= new_row < R and 0 <= new_column < C:
                # check wall
                if grid[new_row][new_column] != '#':
                    # calculate new mask
                    new_mask = mask
                    if (new_row, new_column) in treasure_index:
                        t_idx = treasure_index[(new_row, new_column)]
                        new_mask = mask | (1 << t_idx)
                    
                    new_moves = moves + 1
                    
                    # check if this state is better than what we've seen
                    state_key = (new_row, new_column, new_mask)
                    if state_key not in dp or dp[state_key] > new_moves:
                        dp[state_key] = new_moves
                        queue.append((new_row, new_column, new_moves, new_mask))
    
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
