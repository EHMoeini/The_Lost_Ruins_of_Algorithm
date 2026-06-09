from collections import deque


def bfs_from_cell(grid, R, C, start_row, start_col):
    dist = [[-1] * C for _ in range(R)]
    dist[start_row][start_col] = 0
    
    queue = deque([(start_row, start_col)])
    
    total_distance = 0
    reachable_count = 0
    
    # directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        row, col = queue.popleft()
        current_dist = dist[row][col]
        
        # visit neighbors
        for dr, dc in directions:
            neighbor_row, neighbor_col = row + dr, col + dc
            
            if 0 <= neighbor_row < R and 0 <= neighbor_col < C:
                # check if passable and unvisited
                if grid[neighbor_row][neighbor_col] != '#' and dist[neighbor_row][neighbor_col] == -1:
                    dist[neighbor_row][neighbor_col] = current_dist + 1
                    total_distance += dist[neighbor_row][neighbor_col]
                    reachable_count += 1
                    queue.append((neighbor_row, neighbor_col))
    
    return total_distance, reachable_count


def solve(grid, R, C):
    # find all passable cells
    passable_cells = []
    for row in range(R):
        for col in range(C):
            if grid[row][col] != '#':
                passable_cells.append((row, col))
    
    # if less than 2 passable cells, no valid pairs
    if len(passable_cells) < 2:
        return "0.00"
    
    total_sum = 0
    total_count = 0
    
    for start_row, start_col in passable_cells:
        dist_sum, count = bfs_from_cell(grid, R, C, start_row, start_col)
        total_sum += dist_sum
        total_count += count
    
    # if no valid pairs exist
    if total_count == 0:
        return "0.00"
    
    # calculate average and truncate to 2 decimal places
    average = total_sum / total_count
    
    # truncate without rounding: floor(average * 100) / 100
    import math
    truncated = math.floor(average * 100) / 100
    
    return f"{truncated:.2f}"


def main():
    # get number of rows and columns
    R, C = map(int, input().split())
    
    # get the grid
    grid = []
    for i in range(R):
        row = input().split()
        grid.append(row)
    
    result = solve(grid, R, C)
    print(result)


if __name__ == "__main__":
    main()
