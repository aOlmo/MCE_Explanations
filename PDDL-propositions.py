import pddlpy

def get_predicates(action, human_model):

    final = []

    for eff_prec in ["effect", "precondition"]:

        if eff_prec == "effect":
            operator = "human_model.domain.operators[action.lower()].effect"
        else:
            operator = "human_model.domain.operators[action.lower()].precondition"

        pos_neg_preds = []
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
            pos_neg_preds.append(preds)
        final.append(pos_neg_preds)

    return final


def pddl_to_propositions():
    for action in actions:

        [pos_eff, neg_eff], [pos_pred, neg_pred] = get_predicates(action, human_model)

    return [pos_eff, neg_eff], [pos_pred, neg_pred]


def propositions_to_pddl(actions, pos_eff, neg_eff, pos_pred, neg_pred):

    x = "action_Stack_has_add_effect_clear_?ob"

    actionList = {"pickup":
                    {
                        "precondition": [],
                        "negprecondition": [],
                        "add-effect": [],
                        "delete-effect": []
                    }
                }

    y = x.split("_")
    add_del = y[3]
    effect_prec = y[4]
    objects = " ".join(y[5:])

    if add_del == "add" and effect_prec == "effect":
        actionList["pickup"]['add-effect'].append(objects)
    if add_del == "del" and effect_prec == "effect":
        actionList["pickup"]['delete-effect'].append(objects)
    if add_del == "add" and effect_prec == "precondition":
        actionList["pickup"]['precondition'].append(objects)
    if add_del == "del" and effect_prec == "precondition":
        actionList["pickup"]['negprecondition'].append(objects)

    print(actionList)

    exit()

    template = """
(define (domain blocksworld)
  (:requirements :strips)
(:predicates (clear ?x)
             (on-table ?x)
             (arm-empty)
             (holding ?x)
             (on ?x ?y))

%OPERATORS%
    """

    for action in actions:
        actionList[action] = \
            {
                "parameters": "TODO",
                "precondition": pos_pred,
                "negprecondition": neg_pred,
                "add-effect": pos_eff,
                "delete-effect": neg_eff
            }

        actionList = {"pickup":
                        {
                            "parameters": "?ob",
                            "precondition": ["clear ?ob", "on-table ?ob", "arm-empty"],
                            "negprecondition": [],
                            "add-effect": ["holding ?ob"],
                            "delete-effect": ["clear ?ob", "on-table ?ob", "arm-empty"]
                        }
                  }

    actionString = '\n'.join(['(:action {}\n  :parameters ({})\n  :precondition (and {})\n  :effect (and {}))\n' \
                             .format(key, actionList[key]['parameters'],
                                     ''.join(['({}) '.format(p) for p in actionList[key]['precondition']]) + '' +
                                     ''.join(['(not ({})) '.format(p) for p in actionList[key]['negprecondition']]), \
                                     '{}{}'.format(
                                         ''.join(['({}) '.format(p) for p in actionList[key]['add-effect']]), \
                                         ''.join(
                                             ['(not ({})) '.format(p) for p in actionList[key]['delete-effect']]))) for
                              key in actionList.keys()])


    print(template.replace('%OPERATORS%',actionString))


if __name__ == '__main__':
    human_model = pddlpy.DomainProblem("blocks-domain.pddl", "prob2.pddl")
    actions = ["Pickup", "Putdown", "Stack", "Unstack"]

    [pos_eff, neg_eff], [pos_pred, neg_pred] = pddl_to_propositions()
    propositions_to_pddl(actions, pos_eff, neg_eff, pos_pred, neg_pred)

