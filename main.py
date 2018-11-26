import random
import pddlpy
import time

from aStar import astarSearch
from Problem import Problem
from Propositions import Propositions

models_folder = "models/"
tmp_state_file = models_folder+"tmp_state.pddl"
# Note: since we are using dynamic assignment of variables: hm_name and rm_name
# have to be the names of the human and robot models variables.
hm_name = "human_model"
rm_name = "robot_model"
prob_name = "prob.pddl"
grounded_robot_plan_name = "grounded_robot_plan"


def test_propositions_to_PDDL(human_model, robot_model, hm_name, rm_name):
    prop = Propositions(human_model, robot_model, hm_name, rm_name)

    # Convert the PDDL objects given by pddlpy to a dictionary of propositions
    propositions_dict = prop.pddl_to_propositions(human_model, hm_name)

    # Convert the dictionary to an array of propositions
    array_propos = prop.get_propositions_in_array(propositions_dict)

    # Get parameters
    print(prop.propositions_to_pddl(array_propos))


def search_explanations(xpl_folder, heuristic_flag, domain_template_file, objs_w_underscores):

    total_time = 0
    orig_xpl_folder = xpl_folder

    for xpls in range(2, 5):
        test_folder = orig_xpl_folder + str(xpls)+ "/"

        pddl_hm = test_folder + hm_name + ".pddl"
        pddl_rm = test_folder + rm_name + ".pddl"
        pddl_prob = test_folder + prob_name
        pddl_rplan = test_folder + grounded_robot_plan_name

        human_model = pddlpy.DomainProblem(pddl_hm, pddl_prob)
        robot_model = pddlpy.DomainProblem(pddl_rm, pddl_prob)

        p = Problem(human_model, robot_model, hm_name, rm_name,
                    pddl_rm, pddl_prob, pddl_rplan, tmp_state_file,
                    heuristic_flag, domain_template_file, objs_w_underscores)

        start_time = time.time()
        astarSearch(p)
        elapsed_time = time.time() - start_time

        print("Elapsed time: {} \n".format(elapsed_time))
        total_time += elapsed_time


if __name__ == '__main__':


    heuristic_flag = True
    obj_names_with_underscores_flag = True
    domain_template_file = "models/template_pathway_domain.pddl"
    xpls_folder = models_folder + "test-domains/pathways-propositionl-strips/expl-"
    search_explanations(xpls_folder, heuristic_flag, domain_template_file, obj_names_with_underscores_flag)  #TODO-A: Get the table to fill from this function

    heuristic_flag = False
    search_explanations(xpls_folder, heuristic_flag, domain_template_file, obj_names_with_underscores_flag)

    heuristic_flag = True
    obj_names_with_underscores_flag = False
    domain_template_file = "models/template.pddl"
    xpls_folder = models_folder + "blocksworld/expl-"
    search_explanations(xpls_folder, heuristic_flag, domain_template_file, obj_names_with_underscores_flag)

    heuristic_flag = False
    search_explanations(xpls_folder, heuristic_flag, domain_template_file, obj_names_with_underscores_flag)


