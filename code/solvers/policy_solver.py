import numpy as np
import torch

from lbc.problems.problem import Problem
from lbc.solvers.solver import Solver


class PolicySolver(Solver):

    def __init__(self, policy_oracle):
        super().__init__()
        self.policy_oracle = policy_oracle
        self.solver_name = "NeuralNetwork"

    def policy(self, problem: Problem, root_state):
        action = np.zeros((problem.action_dim, 1))
        for robot in range(problem.num_robots):
            robot_action_idxs = problem.action_idxs[robot]
            policy_encoding = problem.policy_encoding(root_state, robot)
            policy_encoding = torch.tensor(policy_encoding, dtype=torch.float32).squeeze().unsqueeze(0)
            action[robot_action_idxs, 0] = self.policy_oracle[robot](policy_encoding).detach().numpy().squeeze()
        return action
