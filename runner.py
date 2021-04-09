import jnius_config
jnius_config.set_classpath('.', 'hyflex/*')
from jnius import autoclass
import configparser
import argparse
import pathlib
import random
import json
from hhrl.agent import RandomAgent
from hhrl.agent.mab import DMABAgent, FRRMABAgent
from hhrl.agent.rl import DQNAgent
from hhrl.reward import ExtremeValue, ImprovementRate
from hhrl.state import SlidingWindowState
from hhrl.acceptance import AcceptAll
from hhrl.hh import HyperHeuristic


agent_dict = {
        'DQN': DQNAgent,
        'DMAB': DMABAgent,
        'FRRMAB': FRRMABAgent,
        'RAND': RandomAgent,
        }


reward_dict = {
        'EV': ExtremeValue,
        'IR': ImprovementRate,
        }


acceptance_dict = {
        'ALL': AcceptAll,
        }


def output_path(args, config, problem_dict, rootdir=''):
    config_name = args.config.split('/')[-1].split('.')[0]
    instance_name = problem_dict['instances'][str(args.instance_id)]
    return pathlib.Path(f'{rootdir}/{args.problem}/{instance_name}/{args.agent}/{args.reward}/{args.acceptance}/{config_name}')


def main(args):
    config = configparser.ConfigParser()
    config.read(args.config)
    with open(f'problems_json/{args.problem}.json', 'r') as json_file:
        problem_dict = json.load(json_file)
    path = output_path(args, config, problem_dict, rootdir=args.output_dir)
    if (path / f'{args.run_id}.dat').exists() and not args.overwrite:
        return
    seed = random.randint(0,10000)
    ProblemClass = autoclass(problem_dict['class'])
    problem = ProblemClass(seed)
    problem.loadInstance(args.instance_id)
    # problem.setMemorySize(3)
    actions = problem_dict['actions']
    state_env = SlidingWindowState(config, actions)
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
    parser.add_argument('-p', '--problem', type=str, default='VRP')
    parser.add_argument('-c', '--config', type=str, default='configs/default-config.ini')
    parser.add_argument('-o', '--output_dir', type=str, default='tmp')
    parser.add_argument('-i', '--instance_id', type=int, default=0)
    parser.add_argument('-r', '--run_id', type=int, default=0)
    parser.add_argument('-t', '--time_limit', type=int, default=3)
    parser.add_argument('-ag', '--agent', type=str, default='DQN')
    parser.add_argument('-rw', '--reward', type=str, default='IR')
    parser.add_argument('-ac', '--acceptance', type=str, default='ALL')
    parser.add_argument('-ow', '--overwrite', default=False, action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
