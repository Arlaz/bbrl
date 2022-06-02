import sys
import os

import torch
import gym
import my_gym

from omegaconf import DictConfig
from bbrl.workspace import Workspace
from bbrl.utils.replay_buffer import ReplayBuffer
from bbrl.agents import Agents, TemporalAgent, PrintAgent
from bbrl.agents.agent import Agent
from bbrl.agents.gyma import AutoResetGymAgent
from bbrl import instantiate_class, get_class, get_arguments
import hydra

from bbrl.utils.chrono import Chrono

# HYDRA_FULL_ERROR = 1


class AutoResetEnvAgent(AutoResetGymAgent):
    # Create the environment agent
    # This agent implements N gym environments with auto-reset
    def __init__(self, cfg, n_envs):
        super().__init__(get_class(cfg.gym_env), get_arguments(cfg.gym_env), n_envs)
        env = instantiate_class(cfg.gym_env)
        env.seed(cfg.algorithm.seed)
        self.observation_space = env.observation_space
        self.action_space = env.action_space
        del env


class ActionAgent(Agent):
    # Create the action agent
    def __init__(self):
        super().__init__()

    def forward(self, t, **kwargs):
        action = torch.tensor([0])
        self.set(("action", t), action)


def make_gym_env(env_name):
    return gym.make(env_name)


def run_rb(cfg):

    train_env_agent = AutoResetEnvAgent(cfg, n_envs=cfg.algorithm.n_envs)
    action_agent = ActionAgent()

    # Compose both previous agents
    tr_agent = Agents(train_env_agent, action_agent)

    # Get a temporal agent that can be executed in a workspace
    train_agent = TemporalAgent(tr_agent)

    train_workspace = Workspace()  # Used for training
    rb = ReplayBuffer(max_size=6)

    nb_steps = 0

    # 7) Training loop
    for epoch in range(cfg.algorithm.max_epochs):
        # Execute the agent in the workspace
        if epoch > 0:
            train_workspace.zero_grad()
            train_workspace.copy_n_last_steps(1)
            train_agent(
                train_workspace, t=1, n_steps=cfg.algorithm.n_steps - 1, stochastic=True
            )
        else:
            train_agent(
                train_workspace, t=0, n_steps=cfg.algorithm.n_steps, stochastic=True
            )

        nb_steps += cfg.algorithm.n_steps * cfg.algorithm.n_envs

        transition_workspace = train_workspace.get_transitions()

        obs = transition_workspace["env/env_obs"]
        print("obs ante:", obs)

        rb.put(transition_workspace)
        rb.print_obs()

        rb_workspace = rb.get_shuffled(cfg.algorithm.batch_size)

        obs = rb_workspace["env/env_obs"]
        print("obs post:", obs)


def main_loop(cfg):
    chrono = Chrono()
    logdir = "./plot/"
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    run_rb(cfg)
    chrono.stop()


@hydra.main(config_path="./configs/", config_name="rb_test.yaml", version_base="1.1")
def main(cfg: DictConfig):
    # print(OmegaConf.to_yaml(cfg))
    torch.manual_seed(cfg.algorithm.seed)
    main_loop(cfg)


if __name__ == "__main__":
    sys.path.append(os.getcwd())
    main()
