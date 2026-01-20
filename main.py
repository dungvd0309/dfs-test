from map import Map

# --- MAIN PROGRAM ---
if __name__ == "__main__":
    ROWS, COLS = 10, 10
    START_POS = (0, 0)
    GOAL_POS = (8, 8)

    # Create grid
    myMap = Map(ROWS, COLS)

    # Set start and goal
    myMap.set_start(START_POS)
    myMap.set_goal(GOAL_POS)

    # Set obstacles
    OBSTACLES = [(1,1),(2,1),(3,1),
                 (4,4),(5,4),(6,4),
                 (4,5),(5,5),(6,5),
                 (4,6),(5,6),(6,6),]
    myMap.set_obstacles(OBSTACLES)
    print(myMap)
    solution = myMap.dfs_solve()
    print(myMap)
    print("Solution: {}", solution)

    myMap.visualize()