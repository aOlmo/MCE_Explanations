import pddlpy


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


#####################################################################
# search()
#####################################################################
# def search(human_model):
#     # Get the differences between robot model and human's with propositions
#     h_props = get_propositions_in_array(pddl_to_propositions("human_model"))
#     r_props = get_propositions_in_array(pddl_to_propositions("robot_model"))
#
#     # Get default parameters from the human or robot models
#     # Note: We have assumed that both have the same
#     parameters = get_parameters(human_model)
#
#     h_props = set(h_props)
#     r_props = set(r_props)
#
#     diffs = list(r_props.difference(h_props))
#
#     # The nodes of the search tree will have one proposition at a time:
#     # Add to the human model, one proposition and try
#     # TODO: DO BFS
#     node = list(h_props)
#     for diff in diffs:
#         node.append(diff)
#         print(propositions_to_pddl(node, parameters))
#         # Execute VAL
#         # Execute FD
#         # If it works, we will output that as an explanation
#         # If it does not work, we will try adding one proposition and the next one
#
#     pass


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
        self.startState = pddl_to_propositions("human_model")
        self.goalState = pddl_to_propositions("robot_model")

    def getStartState(self):
        return self.startState

    def heuristic(self, state):
        return 0.0

    def isGoal(self, state):



    def getSuccessors(self, node):
        listOfSuccessors = []

        state = set(node)
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


####################################################
# ------------------------------------------------ #
####################################################







####################################################
#                       MAIN                       #
####################################################
if __name__ == '__main__':
    models_folder = "models/"
    model_name = "human_model"

    human_model = pddlpy.DomainProblem(models_folder+"human-model-simple.pddl", models_folder+"prob.pddl")
    robot_model = pddlpy.DomainProblem(models_folder+"robot-model.pddl", models_folder+"prob.pddl")

    a = Problem()
    print(a.dist)

    # test_propositions_to_PDDL(human_model)

    # Perform the search for the Minimum Explanation
    # search(human_model, robot_model)
