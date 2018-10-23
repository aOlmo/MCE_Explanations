import pddlpy
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
    problem_file = "models/prob.pddl"
    tmp_state_file = "models/tmp_state.pddl"

    pddl_rm = models_folder+"robot-model.pddl"
    pddl_prob = models_folder+"prob.pddl"
    pddl_rplan = models_folder+"grounded_robot_plan"


    # Note: since we are using dynamic assignment of variables: hm_name and rm_name
    # have to be the names of the human and robot models variables.
    hm_name = "human_model"
    rm_name = "robot_model"
    human_model = pddlpy.DomainProblem(models_folder + "human-model-simple.pddl", models_folder + "prob.pddl")
    robot_model = pddlpy.DomainProblem(models_folder + "robot-model.pddl", models_folder + "prob.pddl")

    p = Problem(human_model, robot_model, hm_name, rm_name,
                pddl_rm, pddl_prob, pddl_rplan, tmp_state_file)

    astarSearch(p)

    # ----------------------------  #
    # test_propositions_to_PDDL(human_model, robot_model, "human_model", "robot_model")


