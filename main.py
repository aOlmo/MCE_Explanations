import pddlpy
import time
from aStar import astarSearch
from Problem import Problem
from Propositions import Propositions


def test_propositions_to_PDDL(human_model, robot_model, hm_name, rm_name):
    prop = Propositions(human_model, robot_model, hm_name, rm_name)

    # Convert the PDDL objects given by pddlpy to a dictionary of propositions
    propositions_dict = prop.pddl_to_propositions(human_model, hm_name)

    # Convert the dictionary to an array of propositions
    array_propos = prop.get_propositions_in_array(propositions_dict)

    # Get parameters
    print(prop.propositions_to_pddl(array_propos))


if __name__ == '__main__':
    models_folder = "models/"
    test_folder = "models/test/"
    tmp_state_file = models_folder+"tmp_state.pddl"

    # pddl_rm = models_folder+"test-robot-model.pddl"
    # pddl_prob = models_folder+"test-prob.pddl"
    # pddl_rplan = models_folder+"test-grounded_robot_plan"

    pddl_hm = test_folder + "human-model.pddl"
    pddl_rm = test_folder + "robot-model.pddl"
    pddl_prob = test_folder + "prob.pddl"
    pddl_rplan = test_folder + "grounded_robot_plan"
    # Note: since we are using dynamic assignment of variables: hm_name and rm_name
    # have to be the names of the human and robot models variables.
    hm_name = "human_model"
    rm_name = "robot_model"
    human_model = pddlpy.DomainProblem(pddl_hm, pddl_prob)
    robot_model = pddlpy.DomainProblem(pddl_rm, pddl_prob)

    p = Problem(human_model, robot_model, hm_name, rm_name,
                pddl_rm, pddl_prob, pddl_rplan, tmp_state_file)

    start_time = time.time()
    astarSearch(p)
    elapsed_time = time.time() - start_time
    print("Elapsed time: ", elapsed_time)

    # ----------------------------  #
    # test_propositions_to_PDDL(human_model, robot_model, "human_model", "robot_model")


