import os
import copy
import pddlpy
from aStar import astarSearch
from problem import Problem

template = """
(define (domain blocksworld)
  (:requirements :strips)
(:predicates (clear ?x)
             (on-table ?x)
             (holding ?x)
             (on ?x ?y))

%OPERATORS%)"""


#####################################################################
# get_propositions_from_model()
#####################################################################
def get_propositions_from_action(action, model_name):
    final = []
    for eff_prec in ["effect", "precondition"]:

        if eff_prec == "effect":
            operator = model_name+".domain.operators[action].effect"
        else:
            operator = model_name+".domain.operators[action].precondition"

        pos_neg_precs = []
        for add_del in ["add", "del"]:
            preds = []
            if add_del == "add":
                list_eff = eval(operator+"_pos")
            else:
                list_eff = eval(operator+"_neg")

            for atom in list_eff:
                pred = atom.predicate
                aux = ""
                for i in pred:
                    aux += "_" + i

                preds.append("action_"+action+"_has_"+add_del+"_"+eff_prec+aux)
            pos_neg_precs.append(preds)
        final.append(pos_neg_precs)

    return final


#####################################################################
# pddl_to_propositions()
#####################################################################
def pddl_to_propositions(model_name):
    # Note: We assume that human and robot actions are the same
    actions = list(human_model.operators())

    prop_dict = {}
    for action in actions:
        [pos_eff, neg_eff], [pos_prec, neg_prec] = get_propositions_from_action(action, model_name)
        prop_dict[action] = {
            "pos_eff": pos_eff,
            "neg_eff": neg_eff,
            "pos_prec": pos_prec,
            "neg_prec": neg_prec
        }

    return prop_dict


#####################################################################
# def propositions_to_pddl()
#####################################################################
def propositions_to_pddl(propositions, parameters):
    actionList = {}
    for prop in propositions:
        aux = prop.split("_")
        action = aux[1]
        add_del = aux[3]
        effect_prec = aux[4]
        objects = " ".join(aux[5:])

        if not actionList.get(action):
            actionList[action] = {
                "parameters": " ".join(parameters[action]),
                "precondition": [],
                "negprecondition": [],
                "add-effect": [],
                "delete-effect": []
            }

        if add_del == "add" and effect_prec == "precondition":
            actionList[action]['precondition'].append(objects)
        if add_del == "del" and effect_prec == "precondition":
            actionList[action]['negprecondition'].append(objects)
        if add_del == "add" and effect_prec == "effect":
            actionList[action]['add-effect'].append(objects)
        if add_del == "del" and effect_prec == "effect":
            actionList[action]['delete-effect'].append(objects)

    actionString = '\n'.join(['(:action {}\n  :parameters ({})\n  :precondition (and {})\n  :effect (and {}))\n'
                             .format(key, actionList[key]['parameters'],
                                     ''.join(['({}) '.format(p) for p in actionList[key]['precondition']]) + '' +
                                     ''.join(['(not ({})) '.format(p) for p in actionList[key]['negprecondition']]),
                                     '{}{}'.format(
                                         ''.join(['({}) '.format(p) for p in actionList[key]['add-effect']]),
                                         ''.join(
                                             ['(not ({})) '.format(p) for p in actionList[key]['delete-effect']]))) for
                              key in actionList.keys()])
    return template.replace('%OPERATORS%',actionString)


#####################################################################
# get_propositions_in_array()
#####################################################################
def get_propositions_in_array(propositions_dict):
    ret = []
    for action in propositions_dict.keys():
        for key in propositions_dict[action].keys():
            for t in propositions_dict[action][key]:
                ret.append(t)
    return ret


#####################################################################
# get_parameters()
#####################################################################
def get_parameters(model):
    actions = list(model.operators())

    parameters = {}
    for action in actions:
        parameters[action] = list(model.domain.operators[action].variable_list.keys())
    return parameters

#####################################################################
# test_propositions_to_PDDL()
#####################################################################
def test_propositions_to_PDDL(human_model):
    model_name = "human_model"
    # Convert the PDDL objects given by pddlpy to a dictionary of propositions
    propositions_dict = pddl_to_propositions(model_name)
    # Convert the dictionary to an array of propositions
    array_propos = get_propositions_in_array(propositions_dict)

    # Get parameters
    parameters = get_parameters(human_model)
    print(propositions_to_pddl(array_propos, parameters))



def get_distance():
    h_props = get_propositions_in_array(pddl_to_propositions("human_model"))
    r_props = get_propositions_in_array(pddl_to_propositions("robot_model"))

    h_props = set(h_props)
    r_props = set(r_props)

    diffs = list(r_props.difference(h_props))

    return len(diffs)


####################################################
#                   PROBLEM CLASS                  #
####################################################
class Problem():
    def __init__(self):
        # TODO: The human_model and robot_model are taken
        # from the outter scope. This can be improved
        self.human_model = human_model
        self.robot_model = robot_model
        self.dist = get_distance()
        self.startState = get_propositions_in_array(pddl_to_propositions("human_model"))
        self.goalState = get_propositions_in_array(pddl_to_propositions("robot_model"))
        self.currState = self.startState
        self.cost = self.get_plan("models/robot-model.pddl", "models/prob.pddl")[1]
        self.groundedRobotPlanFile = "models/grounded_robot_plan"

    def get_plan(self, domain_file, problem_file):
        output = os.popen("./scripts/fdplan.sh {} {}".format(domain_file, problem_file)).read().strip()
        plan = [item.strip() for item in output.split('\n')] if output != '' else []

        with open("sas_plan", "r") as cost:
            cost_number = cost.read().split("cost = ")[1][0]

        return plan, cost_number

    def validate_plan(self, domain_file, problem_file, plan_file):
        output = os.popen("./scripts/valplan.sh {} {} {} "
                          .format(domain_file, problem_file, plan_file)).read().strip()
        if "successfully" in output:
            return True
        return False


    def write_domain_file_from_state(self, state, tmp_state_file, problem_file):
        tmp_domain = open(tmp_state_file, "w")
        tmp_problem = open(problem_file)

        pddl_state = propositions_to_pddl(state, parameters)
        tmp_domain.write(pddl_state)

        tmp_domain.close()
        tmp_domain = open(tmp_state_file, "r")

        return tmp_domain.read(), tmp_problem.read()

    def isGoal(self, state):
        tmp_domain, tmp_problem = self.write_domain_file_from_state(state, tmp_state_file, problem_file)
        feasibility_flag = self.validate_plan(tmp_state_file, problem_file, self.groundedRobotPlanFile)
        if not feasibility_flag:
            plan = []
            return (False, plan)

        plan, cost = self.get_plan(tmp_state_file, problem_file)
        optimality_flag = cost == self.cost
        return (optimality_flag, plan)

    def getSuccessors(self, node, old_plan=None):
        # if self.heuristic_flag:
        # return self.heuristic_successors(node, old_plan)
        return self.ordinary_successors(node)

    def ordinary_successors(self, node, old_plan = None):
        listOfSuccessors = []

        state = set(node[0])
        ground_state = set(copy.copy(self.goalState))

        add_set = ground_state.difference(state)
        del_set = state.difference(ground_state)

        for item in add_set:
            new_state = copy.deepcopy(state)
            new_state.add(item)
            listOfSuccessors.append([list(new_state), item])

        for item in del_set:
            new_state = copy.deepcopy(state)
            new_state.remove(item)
            listOfSuccessors.append([list(new_state), item])

        return listOfSuccessors

    def getStartState(self):
        return self.startState

    def heuristic(self, state):
        return 0.0




####################################################
# ------------------------------------------------ #
####################################################




####################################################
#                       MAIN                       #
####################################################
if __name__ == '__main__':
    models_folder = "models/"
    model_name = "human_model"
    tmp_state_file = "models/temp_state.pddl"
    problem_file = "models/prob.pddl"

    human_model = pddlpy.DomainProblem(models_folder+"human-model-simple.pddl", models_folder+"prob.pddl")
    robot_model = pddlpy.DomainProblem(models_folder+"robot-model.pddl", models_folder+"prob.pddl")

    # Get default parameters from the human or robot models
    # Note: We have assumed that both have the same
    parameters = get_parameters(human_model)

    c = [['action_pickup_has_del_effect_on-table_?ob', 'action_pickup_has_add_effect_holding_?ob', 'action_unstack_has_add_precondition_clear_?ob', 'action_unstack_has_del_effect_on_?ob_?underob', 'action_pickup_has_add_precondition_clear_?ob', 'action_putdown_has_add_precondition_holding_?ob', 'action_unstack_has_add_effect_clear_?underob', 'action_unstack_has_add_effect_holding_?ob', 'action_pickup_has_del_effect_clear_?ob', 'action_stack_has_add_precondition_holding_?ob', 'action_stack_has_add_effect_on_?ob_?underob', 'action_stack_has_del_effect_holding_?ob', 'action_stack_has_del_effect_clear_?underob', 'action_putdown_has_del_effect_holding_?ob', 'action_putdown_has_add_effect_on-table_?ob', 'action_unstack_has_add_precondition_on_?ob_?underob', 'action_unstack_has_del_effect_clear_?ob', 'action_stack_has_add_precondition_clear_?underob', 'action_putdown_has_add_effect_clear_?ob', 'action_stack_has_add_effect_clear_?ob'], ['action_stack_has_add_precondition_holding_?ob']]

    # print(propositions_to_pddl(c[0], parameters))

    p = Problem()

    astarSearch(p)
