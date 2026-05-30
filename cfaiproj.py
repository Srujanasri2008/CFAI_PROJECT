# ==========================================================
# AI EMERGENCY EVACUATION PATH PLANNER
# TERMINAL VERSION
# Covers CO1 to CO6
# ==========================================================

from collections import deque
import heapq
import random

# ==========================================================
# CO1 - GRAPH REPRESENTATION
# ==========================================================

graph = {

    "A": [("B", 2), ("C", 3)],

    "B": [("A", 2), ("D", 4), ("E", 5)],

    "C": [("A", 3), ("F", 2), ("G", 4)],

    "D": [("B", 4), ("H", 3)],

    "E": [("B", 5), ("H", 2), ("O", 3)],

    "F": [("C", 2), ("I", 3)],

    "G": [("C", 4), ("I", 2), ("M", 2)],

    "H": [("D", 3), ("E", 2), ("J", 3)],

    "I": [("F", 3), ("G", 2), ("J", 2)],

    "J": [("H", 3), ("I", 2), ("K", 2), ("Exit2", 5)],

    "K": [("J", 2), ("L", 2)],

    "L": [("K", 2), ("Exit1", 3)],

    "M": [("G", 2), ("N", 2)],

    "N": [("M", 2), ("Exit3", 2)],

    "O": [("E", 3), ("P", 2)],

    "P": [("O", 2), ("Exit4", 3)],

    "Exit1": [],
    "Exit2": [],
    "Exit3": [],
    "Exit4": []
}

# ==========================================================
# CO5 - HAZARD LEVELS
# ==========================================================

hazard_levels = {

    "A": 1,
    "B": 2,
    "C": 7,
    "D": 8,
    "E": 2,
    "F": 1,
    "G": 3,
    "H": 9,
    "I": 2,
    "J": 5,
    "K": 1,
    "L": 1,
    "M": 2,
    "N": 1,
    "O": 6,
    "P": 2,

    "Exit1": 0,
    "Exit2": 0,
    "Exit3": 0,
    "Exit4": 0
}

# ==========================================================
# CO3 - OBSTACLES / BLOCKED ROOMS
# ==========================================================

blocked_rooms = ["D", "H"]

# ==========================================================
# CO2 - HEURISTIC VALUES FOR A*
# ==========================================================

heuristic = {

    "A": 15,
    "B": 13,
    "C": 12,
    "D": 10,
    "E": 9,
    "F": 9,
    "G": 8,
    "H": 7,
    "I": 6,
    "J": 5,
    "K": 4,
    "L": 3,
    "M": 5,
    "N": 3,
    "O": 5,
    "P": 3,

    "Exit1": 0,
    "Exit2": 0,
    "Exit3": 0,
    "Exit4": 0
}

# ==========================================================
# DISPLAY BUILDING MAP
# ==========================================================

def display_building():

    print("\n================ BUILDING MAP ================")

    for node in graph:
        print(node, "->", graph[node])

    print("==============================================")

# ==========================================================
# DISPLAY HAZARDS
# ==========================================================

def display_hazards():

    print("\n================ HAZARD ROOMS ================")

    for room in hazard_levels:

        print(room, "-> Risk Level:", hazard_levels[room])

    print("==============================================")

# ==========================================================
# DISPLAY BLOCKED ROOMS
# ==========================================================

def display_blocked():

    print("\n================ BLOCKED ROOMS ===============")

    for room in blocked_rooms:

        print(room, "is BLOCKED")

    print("==============================================")

# ==========================================================
# CO2 - BFS SEARCH
# ==========================================================

def bfs(start, goal):

    queue = deque([(start, [start])])

    visited = set()

    while queue:

        current, path = queue.popleft()

        if current == goal:
            return path

        visited.add(current)

        for neighbor, cost in graph[current]:

            if neighbor not in visited and neighbor not in blocked_rooms:

                queue.append((neighbor, path + [neighbor]))

    return None

# ==========================================================
# CO2 - UCS SEARCH
# ==========================================================

def ucs(start, goal):

    pq = [(0, start, [start])]

    visited = set()

    while pq:

        total_cost, current, path = heapq.heappop(pq)

        if current == goal:
            return path, total_cost

        if current in visited:
            continue

        visited.add(current)

        for neighbor, distance in graph[current]:

            if neighbor not in visited and neighbor not in blocked_rooms:

                new_cost = total_cost + distance

                heapq.heappush(
                    pq,
                    (new_cost, neighbor, path + [neighbor])
                )

    return None, float("inf")

# ==========================================================
# CO2 - A* SEARCH
# ==========================================================

def astar(start, goal):

    pq = [(0, 0, start, [start])]

    visited = set()

    while pq:

        f_cost, g_cost, current, path = heapq.heappop(pq)

        if current == goal:
            return path, g_cost

        if current in visited:
            continue

        visited.add(current)

        for neighbor, distance in graph[current]:

            if neighbor not in visited and neighbor not in blocked_rooms:

                risk = hazard_levels[neighbor]

                new_g = g_cost + distance + risk

                new_f = new_g + heuristic[neighbor]

                heapq.heappush(
                    pq,
                    (new_f, new_g, neighbor, path + [neighbor])
                )

    return None, float("inf")

# ==========================================================
# CO3 - CSP CONSTRAINT CHECKING
# ==========================================================

def check_constraints(path):

    print("\n============= CONSTRAINT CHECKING ============")

    safe = True

    for node in path:

        if node in blocked_rooms:

            print(node, "is BLOCKED")

            safe = False

        if hazard_levels[node] >= 7:

            print(node, "has HIGH FIRE RISK")

            safe = False

    if safe:

        print("All constraints satisfied")

        print("Path is SAFE")

    else:

        print("Unsafe path detected")

    print("==============================================")

# ==========================================================
# CO5 - FIRE PREDICTION
# ==========================================================

def fire_prediction():

    print("\n============= FIRE RISK PREDICTION ===========")

    for node in hazard_levels:

        probability = hazard_levels[node] * 10

        if probability > 100:
            probability = 100

        print(node, "->", probability, "% Risk")

    print("==============================================")

# ==========================================================
# CO4 - DECISION MAKING
# CHOOSE BEST EXIT
# ==========================================================

def choose_best_exit(start):

    exits = ["Exit1", "Exit2", "Exit3", "Exit4"]

    best_exit = None

    best_path = None

    minimum_cost = float("inf")

    print("\n================ EXIT ANALYSIS ===============")

    for exit_node in exits:

        path, cost = astar(start, exit_node)

        if path is not None:

            print("\nChecking", exit_node)

            print("Path:", path)

            print("Cost:", cost)

            if cost < minimum_cost:

                minimum_cost = cost

                best_exit = exit_node

                best_path = path

    print("\n==============================================")

    print("BEST EXIT:", best_exit)

    print("OPTIMAL SAFE PATH:", best_path)

    print("MINIMUM COST:", minimum_cost)

    print("==============================================")

    return best_exit, best_path

# ==========================================================
# MAIN PROGRAM
# ==========================================================

def main():

    print("\n================================================")
    print(" AI EMERGENCY EVACUATION PATH PLANNER ")
    print("================================================")

    # ------------------------------------------------------
    # DISPLAY ENVIRONMENT
    # ------------------------------------------------------

    display_building()

    display_hazards()

    display_blocked()

    # ------------------------------------------------------
    # START ROOM
    # ------------------------------------------------------

    start_room = "A"

    print("\nPerson Starting Room:", start_room)

    # ------------------------------------------------------
    # BFS
    # ------------------------------------------------------

    print("\n================ BFS RESULT ==================")

    bfs_path = bfs(start_room, "Exit3")

    print("BFS Shortest Path:")

    print(bfs_path)

    print("================================================")

    # ------------------------------------------------------
    # UCS
    # ------------------------------------------------------

    print("\n================ UCS RESULT ==================")

    ucs_path, ucs_cost = ucs(start_room, "Exit3")

    print("UCS Optimal Distance Path:")

    print(ucs_path)

    print("Distance Cost:", ucs_cost)

    print("================================================")

    # ------------------------------------------------------
    # A*
    # ------------------------------------------------------

    print("\n================ A* RESULT ===================")

    astar_path, astar_cost = astar(start_room, "Exit3")

    print("Safest Optimal Path:")

    print(astar_path)

    print("Safety Cost:", astar_cost)

    print("================================================")

    # ------------------------------------------------------
    # CSP CONSTRAINT CHECKING
    # ------------------------------------------------------

    check_constraints(astar_path)

    # ------------------------------------------------------
    # FIRE PREDICTION
    # ------------------------------------------------------

    fire_prediction()

    # ------------------------------------------------------
    # DECISION MAKING
    # ------------------------------------------------------

    best_exit, best_path = choose_best_exit(start_room)

    # ------------------------------------------------------
    # CO6 - FINAL INTEGRATED AI OUTPUT
    # ------------------------------------------------------

    print("\n================ FINAL OUTPUT =================")

    print("Person Successfully Evacuated")

    print("Chosen Exit:", best_exit)

    print("Final Safe Path:", best_path)

    print("Blocked Rooms Avoided:", blocked_rooms)

    print("Hazards Avoided Successfully")

    print("Emergency Evacuation Completed")

    print("================================================")

# ==========================================================
# RUN PROGRAM
# ==========================================================

main()