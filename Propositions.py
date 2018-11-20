# template = """
# (define (domain BLOCKS)
#   (:requirements :strips)
#   (:predicates (on ?x ?y)
#            (ontable ?x)
#            (clear ?x)
#            (handempty)
#            (holding ?x))
#
# %OPERATORS%)
# """
# template = open("models/template.pddl").read()

template = open("models/template_pathway_domain.pddl").read()

class Propositions(object):
    def __init__(self, human_model, robot_model, hm_name, rm_name):
        self.human_model = human_model
        self.robot_model = robot_model
        self.hm_name = hm_name
        self.rm_name = rm_name

        # Note: Assuming that H and R have the same parameters/actions
        self.parameters = self.get_parameters(human_model)
        self.actions = list(human_model.operators())

    def get_propositions_from_action(self, action, model_name):
        final = []
        for eff_prec in ["effect", "precondition"]:

            if eff_prec == "effect":
                operator = "self." + model_name + ".domain.operators[action].effect"
            else:
                operator = "self." + model_name + ".domain.operators[action].precondition"

            pos_neg_precs = []
            for add_del in ["add", "del"]:
                preds = []
                if add_del == "add":
                    list_eff = eval(operator + "_pos")
                else:
                    list_eff = eval(operator + "_neg")

                for atom in list_eff:
                    pred = atom.predicate
                    aux = ""
                    for i in pred:
                        aux += "_" + i

                    preds.append("action_" + action + "_has_" + add_del + "_" + eff_prec + aux)
                pos_neg_precs.append(preds)
            final.append(pos_neg_precs)

        return final

    def pddl_to_propositions(self, model_name):
        prop_dict = {}
        for action in self.actions:
            [pos_eff, neg_eff], [pos_prec, neg_prec] = self.get_propositions_from_action(action, model_name)
            prop_dict[action] = {
                "pos_eff": pos_eff,
                "neg_eff": neg_eff,
                "pos_prec": pos_prec,
                "neg_prec": neg_prec
            }

        return prop_dict

    def propositions_to_pddl(self, propositions):
        actionList = {}
        for prop in propositions:
            action = prop.replace("action_", "").split("_has")[0]
            add_del = "add" if "_add_" in prop else "del"
            effect_prec = "effect" if "_effect_" in prop else "precondition"
            objects = prop.split(effect_prec+"_")[1]

            if not actionList.get(action):
                actionList[action] = {
                    "parameters": " ".join(self.parameters[action]),
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
                                                 ['(not ({})) '.format(p) for p in actionList[key]['delete-effect']])))
                                  for key in actionList.keys()])

        return template.replace('%OPERATORS%', actionString)

    def get_propositions_in_array(self, propositions_dict):
        ret = []
        for action in propositions_dict.keys():
            for key in propositions_dict[action].keys():
                for t in propositions_dict[action][key]:
                    ret.append(t)
        return ret

    def get_parameters(self, model):
        actions = list(model.operators())

        parameters = {}
        for action in actions:
            parameters[action] = list(model.domain.operators[action].variable_list.keys())
        return parameters

    def get_distance(self):
        h_props = self.get_propositions_in_array(self.pddl_to_propositions(self.hm_name))
        r_props = self.get_propositions_in_array(self.pddl_to_propositions(self.rm_name))

        h_props = set(h_props)
        r_props = set(r_props)

        diffs = list(r_props.difference(h_props))

        return len(diffs)
