import os
import sys
import numpy as np
import argparse
import time
import torch
import csv
import gym
import MDPs
import Pytorch
import tensorflow as tf
from datetime import datetime

from utils.utils import *

start_time = time.time()

def build_parser():
    parser = argparse.ArgumentParser(description='Temporal Difference Learning Args')
    parser.add_argument('--alg', type=str, default="TDLambda",
                        help='Trace algorithm to be used (default: TDLambda)')
    parser.add_argument('--log_dir', type=str, default="log/",
                        help='Directory for storing logs (default: log/)')
    parser.add_argument('--env', type=str, default="CyclicMDP",
                        help='Toy environment (default: CyclicMDP)')
    parser.add_argument('--lib', type=str, default="torch",
                        help='Deep Learning Library to use (default: torch)')
    parser.add_argument('--eval', type=bool, default=True,
                        help='Evaluates a policy a policy every 10 episode (default: True)')
    parser.add_argument('--gamma', type=float, default=0.99, metavar='G',
                        help='discount factor for reward (default: 0.99)')
    parser.add_argument('--lamb', type=float, default=0.5, metavar='G',
                        help='lambda value for trace updates (default: 0.95)')
    parser.add_argument('--lr', type=float, default=0.001, metavar='G',
                        help='learning rate of agent (default: 0.01)')
    parser.add_argument('--seed', type=int, default=123456, metavar='N',
                        help='random seed (default: 123456)')
    parser.add_argument('--batch_size', type=int, default=32, metavar='N',
                        help='batch size (default: 32)')
    parser.add_argument('--num_steps', type=float, default=10001, metavar='N',
                        help='maximum number of steps (default: 100000)')
    parser.add_argument('--log_interval', type=int, default=500, metavar='N',
                        help='save model and results every xth step (default: 10000)')
    parser.add_argument('--epsilon_start', type=float, default=1,
                        help='Epsilon start for greedy exploration (default: 1)')
    parser.add_argument('--epsilon_final', type=float, default=0.01,
                        help='Epsilon final for greedy exploration (default: 0.01)')
    parser.add_argument('--epsilon_decay', type=float, default=500,
                        help='Epsilon decay for greedy exploration (default: 500)')
    parser.add_argument('--window_size', type=int, default=10,
                        help='Window length for averaging returns in plots (default: 50)')

    return parser


def train(args, env, policy, log_dict):
    replay_buffer = ReplayBuffer(10000)
    state = env.reset()
    loss = torch.FloatTensor([0])
    steps = 0
    ep_step_count = 0
    ep_reward = 0
    ep_loss = 0
    while steps < args.num_steps:
        action = policy.get_actions(steps, state)
        next_state, reward, done, _ = env.step(action)
        ep_reward += reward
        steps += 1
        ep_step_count += 1

        if len(replay_buffer) > args.batch_size:
            loss = policy.update(replay_buffer, steps, ep_step_count)
        ep_loss += loss.item()

        replay_buffer.push(state, action, reward, next_state, done)
        state = next_state

        if done:
            state = env.reset()
            ep_step_count = 0
            done = False
            log_dict['rewards'].append(ep_reward)
            log_dict['td_error'].append(ep_loss)
            if len(log_dict['rewards']) > args.window_size:
                log_dict['average_rewards'].append(np.mean(log_dict['rewards'][-args.window_size]))
                log_dict['average_error'].append(np.mean(log_dict['td_error'][-args.window_size]))
            log_dict['ep_count'].append(steps)
            ep_loss = 0
            ep_reward = 0
        
        if steps % args.log_interval==0:
            print('\tSteps: ', steps,'/', args.num_steps,'\tReward:', 
                log_dict['rewards'][-1],'\tMax Reward:',max(log_dict['rewards']),'\tTD Error:',log_dict['td_error'][-1],'\tTime:', time.time() - start_time)
    
    return log_dict


def main():
    parser = build_parser()
    args = parser.parse_args()
    print(args)

    np.random.seed(args.seed)
    
    if not os.path.exists(args.log_dir):
        print('\tCreating log directory ', args.log_dir)
        os.makedirs(args.log_dir)   

    log_dict = {}
    log_dict['rewards'] = []
    log_dict['average_rewards'] = []
    log_dict['average_error'] = []
    log_dict['td_error'] = []
    log_dict['ep_count'] = []

    env_list = ['CyclicMDP', 'OneStateGaussianMDP', 'OneStateMDP']

    print('\tCreating environment ', args.env)
    if args.env in env_list:
        env = getattr(MDPs, args.env)()
        num_actions = env.num_actions
        state_dims = env.num_states
    else:
        env = gym.make(args.env)
        env.seed(args.seed)
        num_actions = env.action_space.n
        state_dims = env.reset().shape[0]
    print('\tEnvironment created!')

    if args.lib=='torch':
        print('\tFramework set to PyTorch')
        use_cuda = torch.cuda.is_available()
        device = torch.device('cuda' if use_cuda else 'cpu')
        torch.manual_seed(args.seed)
        policy = getattr(Pytorch, args.alg)(args, state_dims, num_actions)
    else:
        print('\tFramework set to Tensorflow 2.0')
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        tf.config.run_functions_eagerly(True)
        tf.random.set_seed(args.seed)
        policy = getattr(Tensorflow, args.alg)(args, state_dims, num_actions)

    log_dict = train(args, env, policy, log_dict)
    res_plot(args, log_dict)
    save_logs(args, log_dict)


if __name__=="__main__":
    main()



