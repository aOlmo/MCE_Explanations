from queue import PriorityQueue

def astarSearch(problem):
    startState = problem.getStartState()
    fringe = PriorityQueue()
    closed = set()
    numberOfNodesExpanded = 0

    fringe.put((problem.heuristic(startState), [startState, []]))

    print("Running aStar Search...")
    while not fringe.empty():

        node = fringe.get()[1]
        goal_check, feasibility_flag, old_plan = problem.is_goal(node[0])

        if goal_check:
            print("Goal Found! Number of Nodes Expanded =", numberOfNodesExpanded)
            print("Explanations:"+str(node[1]))
            print("# Explanations: ", len(node[1]))
            return node[1]

        if frozenset(node[0]) not in closed:

            closed.add(frozenset(node[0]))

            successor_list = problem.getSuccessors(node, feasibility_flag)

            numberOfNodesExpanded += 1

            if not numberOfNodesExpanded % 50:
                print("Number of Nodes Expanded =", numberOfNodesExpanded)

            while successor_list:
                candidate_node = successor_list.pop()
                new_node = [candidate_node[0], node[1] + [candidate_node[1]]]

                fringe.put((problem.heuristic(candidate_node[0]) + len(new_node[1]), new_node))

    return None