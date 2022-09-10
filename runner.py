import configparser
import argparse
import pathlib
import random

from hhrl.agent import RandomAgent
from hhrl.agent.mab import DMABAgent, FRRMABAgent
from hhrl.agent.rl import DQNAgent, DQNUCBAgent, QLearningAgent
from hhrl.reward import *
from hhrl.state import *
from hhrl.acceptance import AcceptAll
from hhrl.hh import HyperHeuristic
from hhrl.problem import *


agent_dict = {
        'DQN': DQNAgent,
        'DMAB': DMABAgent,
        'FRRMAB': FRRMABAgent,
        'RAND': RandomAgent,
        'DQNUCB': DQNUCBAgent,
        'QL': QLearningAgent,
        }


reward_dict = {
        'EV': ExtremeValue,
        'IR': ImprovementRate,
        'DIV': Diversity,
        'IND': ImprovementAndDiversity,
        'IOD': ImprovementOrDiversity,
        'IOP': ImprovementOrPenalty,
        'RIP': RawImprovementPenalty,
        'DIP': DiscreteImprovementPenalty,
        }


state_dict = {
        'SW': [SlidingWindowState],
        'S1': [FitnessImprovementRate, LastActionVector],
        'S2': [UnitaryFitnessDistanceCorrelation, LastActionVector],
        'S3': [LastActionVector],
        'S4': [FitnessImprovementRate, UnitaryFitnessDistanceCorrelation, LastActionVector],
        'S5': [ElapsedTime, LastActionVector],
        'S6': [FitnessImprovementRate, ElapsedTime, LastActionVector],
        'S7': [FitnessImprovementRate, ElapsedTime],
        }


acceptance_dict = {
    'ALL': AcceptAll,
        }


domain_dict = {
        'TSP': TravelingSalesman,
        'FS': FlowShop,
        'SAT': MAXSAT,
        'VRP': VehicleRouting,
        'PS': PersonnelScheduling,
        'BP': BinPacking,
        }


def output_path(args, config, instance_name, rootdir=''):
    config_name = args.config.split('/')[-1].split('.')[0]
    if 'MAB' in args.agent or args.agent == 'RAND':
        state_dir = 'NONE'
    else:
        state_dir = args.state
    return pathlib.Path(f'{rootdir}/{args.problem}/{instance_name}/{args.agent}/{state_dir}/{args.reward}/{args.acceptance}/{config_name}')


def main(args):
    config = configparser.ConfigParser()
    config.read(args.config)
    seed = random.randint(0,10000)
    problem = domain_dict[args.problem](args.instance_id, seed)
    path = output_path(args, config, problem.instance_name, rootdir=args.output_dir)
    if (path / f'{args.run_id}.dat').exists() and not args.overwrite:
        return
    actions = problem.actions
    state_env = StateBuilder(state_dict[args.state], config, actions=actions, time_limit=args.time_limit)
    agent = agent_dict[args.agent](config, actions, state_env=state_env)
    reward = reward_dict[args.reward](config, actions)
    acceptance = acceptance_dict[args.acceptance]()
    hh = HyperHeuristic(problem, agent, reward, acceptance)
    stats = hh.run(args.time_limit)
    stats.run_id = args.run_id
    path.mkdir(parents=True, exist_ok=True)
    stats.save(path)


def parse_args(desc=''):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-p', '--problem', type=str, default='TSP')
    parser.add_argument('-c', '--config', type=str, default='configs/fir_discrete.ini')
    parser.add_argument('-o', '--output_dir', type=str, default='tmp')
    parser.add_argument('-i', '--instance_id', type=int, default=1)
    parser.add_argument('-r', '--run_id', type=int, default=0)
    parser.add_argument('-t', '--time_limit', type=int, default=3)
    parser.add_argument('-ag', '--agent', type=str, default='QL')
    parser.add_argument('-rw', '--reward', type=str, default='RIP')
    parser.add_argument('-st', '--state', type=str, default='S1')
    parser.add_argument('-ac', '--acceptance', type=str, default='ALL')
    parser.add_argument('-ow', '--overwrite', default=False, action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
