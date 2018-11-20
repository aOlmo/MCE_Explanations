### Adding a new domain and problem
1. Get the robot domain and problem: save them as `robot-model.pddl` and `prob.pddl` in a known location
2. Generate robot plan given those two with FastDownward and save it in the same folder with the name grounded\_robot\_plan
3. Make deletions of effects and/or preconditions to `robot-model.pddl` and save them in a new file called `human-model.pddl`
4. Create the template that the algorithm will use (look at Propositions.py for more info)
5. Modify the names of the folders accordingly in `main.py`
