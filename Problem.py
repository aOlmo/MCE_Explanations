import os
import copy
from Propositions import Propositions

class Problem(object):
    def __init__(self, human_model, robot_model, hm_name, rm_name, pddl_rm, pddl_prob, pddl_rplan,
                 tmp_state_file, heuristic_flag, domain_template_file, objs_w_underscores):
        self.human_model = human_model
        self.robot_model = robot_model
        self.hm_name = hm_name
        self.rm_name = rm_name
        self.tmp_state_file = tmp_state_file
        self.pddl_prob = pddl_prob
        self.props = Propositions(human_model, robot_model, hm_name, rm_name, domain_template_file, objs_w_underscores)

        self.dist = self.props.get_distance()

        self.startState = self.props.get_propositions_in_array(self.props.pddl_to_propositions(self.hm_name))
        self.goalState = self.props.get_propositions_in_array(self.props.pddl_to_propositions(self.rm_name))
        self.currState = self.startState

        self.cost = self.get_plan(pddl_rm, self.pddl_prob)[1]
        self.groundedRobotPlanFile = pddl_rplan

        self.heuristic_flag = heuristic_flag

    def get_plan(self, domain, problem):
        output = os.popen("./scripts/fdplan.sh {} {}".format(domain, problem)).read().strip()
        plan = [item.strip() for item in output.split('\n')] if output != '' else []

        with open("sas_plan", "r") as cost:
            cost_val = cost.read().split("cost = ")[1][0]

        return plan, cost_val

    def validate_plan(self, domain_file, problem_file, plan_file):
        output = os.popen("./scripts/valplan.sh {} {} {}"
                          .format(domain_file, problem_file, plan_file)).read().strip()
        if "successfully" in output:
            return True
        return False

    def write_domain_file_from_state(self, state):
        domain = open(self.tmp_state_file, "w")
        pddl_domain = self.props.propositions_to_pddl(state)

        domain.write(pddl_domain)
        domain.close()

        domain = open(self.tmp_state_file)
        problem = open(self.pddl_prob)

        return domain.read(), problem.read()

    def is_goal(self, state):
        # Write the domain and problem files to use them later in FD and VAL
        self.write_domain_file_from_state(state)

        # Validate the plan given the current state and problem files and the grounded plan (pregenerated)
        feasibility_flag = self.validate_plan(self.tmp_state_file, self.pddl_prob, self.groundedRobotPlanFile)
        
        if not feasibility_flag:
            plan = []
            return (False, False, plan)

        plan, cost = self.get_plan(self.tmp_state_file, self.pddl_prob)
        optimality_flag = cost == self.cost
        return (optimality_flag, True, plan)

    def getSuccessors(self, node, feasibility_flag):
        return self.ordinary_successors(node, feasibility_flag)
    

    def ordinary_successors(self, node, feasibility_flag):
        listOfSuccessors = []
        state = set(node[0])
        ground_state = set(copy.copy(self.goalState))

        add_set = ground_state.difference(state)

        if self.heuristic_flag:
            if not feasibility_flag:
                for item in add_set:
                    if "add_effect" in item:
                        new_state = copy.deepcopy(state)
                        new_state.add(item)
                        listOfSuccessors.append([list(new_state), item])

            else:
                for item in add_set:
                    if "precondition" in item:
                        new_state = copy.deepcopy(state)
                        new_state.add(item)
                        listOfSuccessors.append([list(new_state), item])

                    if "del_effect" in item:
                        new_state = copy.deepcopy(state)
                        new_state.add(item)
                        listOfSuccessors.append([list(new_state), item])
        else:
            for item in add_set:
                new_state = copy.deepcopy(state)
                new_state.add(item)
                listOfSuccessors.append([list(new_state), item])

        return listOfSuccessors

    def getStartState(self):
        return self.startState

    def heuristic(self, state):
        return 0.0
