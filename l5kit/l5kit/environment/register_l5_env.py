from pathlib import Path

import gym

from l5kit.environment import reward
from l5kit.simulation.dataset import SimulationConfig
from l5kit.environment.cle_metricset import L5GymCLEMetricSet


def create_l5_env(args):
    """ Create and Register the L5Kit Gym-compatible environment """

    # config path
    env_config_path = Path(args.env_config_path)

    # Closed loop environment
    close_loop_envt = not args.disable_cle

    # Define Reward Function
    if close_loop_envt:
        reward_fn = reward.CLE_Reward(rew_clip_thresh=args.rew_clip)
    else:
        reward_fn = reward.OLE_Reward()

    # Define Close-Loop Simulator
    num_simulation_steps = args.eps_length
    sim_cfg = SimulationConfig(use_ego_gt=False, use_agents_gt=True, disable_new_agents=False,
                               distance_th_far=30, distance_th_close=15,
                               num_simulation_steps=num_simulation_steps,
                               start_frame_index=0, show_info=True)

    # Register L5 Env
    gym.envs.register(
        id='L5-CLE-v0',
        entry_point="l5kit.environment.envs:L5Env",
        kwargs={'env_config_path': env_config_path,
                'sim_cfg': sim_cfg,
                'reward': reward_fn,
                'cle': close_loop_envt},
    )
