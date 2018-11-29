from queue import PriorityQueue

def astarSearch(problem):
    startState = problem.getStartState()
    fringe = PriorityQueue()
    closed = set()
    numberOfNodesExpanded = 0

    fringe.put((problem.heuristic(startState), [startState, []]))

    print("\nRunning aStar Search...")
    while not fringe.empty():

        node = fringe.get()[1]
        goal_check, feasibility_flag, old_plan = problem.is_goal(node[0])

        if goal_check:
            print("Goal Found! # of nodes expanded = {} # of explanations = {} ".format(numberOfNodesExpanded, len(node[1])))
            for i, xpl in enumerate(node[1]):
                print("Explanation {} >> {}".format(i+1, xpl))
            print("")
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