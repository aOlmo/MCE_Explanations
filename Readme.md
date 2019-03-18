### Adding a new domain and problem
1. Get the robot domain and problem: save them as `robot-model.pddl` and `prob.pddl` in a known location
2. Generate robot plan given those two with FastDownward and save it in the same folder with the name grounded\_robot\_plan
3. Make deletions of effects and/or preconditions to `robot-model.pddl` and save them in a new file called `human-model.pddl`
4. Create the template that the algorithm will use (look at Propositions.py for more info)
5. Modify the names of the folders accordingly in `main.py`

### Resources
* PDDL online editor: http://editor.planning.domains/
* More domains https://github.com/potassco/pddl-instances/

### Dependencies
* Python 3+: A version of Python 3 or above.
* Pddlpy: Library made for converting PDDL models in Python objects (more tractable format).
* Fast Downward: Planner used to generate the plans given the domain and problem files.
* VAL: Validator that checks for the plan's feasibility.
* PrettyTable: Needed for the outputs.

### Contributors
* (https://github.com/zahrazahedi28)[Zahra Zahedi] was also a contributor to this project. 
