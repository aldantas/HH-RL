import jnius_config
jnius_config.set_classpath('.', 'hyflex/*')
from jnius import autoclass
import configparser
import random
import argparse
import csv
import os
from hhrl.agent.mab import DMABAgent, FRRMABAgent
from hhrl.agent.rl import DQNAgent
from hhrl.reward import ExtremeValue, ImprovementRate
from hhrl.state import SlidingWindowState
from hhrl.acceptance import AcceptAll
from hhrl.hh import HyperHeuristic


vrp_instances = {
        0: 'Solomon_100_customer_instances/RC207',
        1: 'Solomon_100_customer_instances/R101',
        2: 'Solomon_100_customer_instances/RC103',
        3: 'Solomon_100_customer_instances/R201',
        4: 'Solomon_100_customer_instances/R106',
        5: 'Homberger_1000_customer_instances/C1_10_1',
        6: 'Homberger_1000_customer_instances/RC2_10_1',
        7: 'Homberger_1000_customer_instances/R1_10_1',
        8: 'Homberger_1000_customer_instances/C1_10_8',
        9: 'Homberger_1000_customer_instances/RC1_10_5',
        }


problem_dict = {
        'VRP': 'VRP.VRP',
        'BP': 'BinPacking.BinPacking',
        'SAT': 'SAT.SAT',
        'FS': 'FlowShop.FlowShop',
        'TSP': 'travelingSalesmanProblem.TSP',
        }


agent_dict = {
        'DQN': DQNAgent,
        'DMAB': DMABAgent,
        'FRRMAB': FRRMABAgent,
        }


reward_dict = {
        'EV': ExtremeValue,
        'IR': ImprovementRate,
        }


acceptance_dict = {
        'ALL': AcceptAll,
        }


def output_dir(args, config, rootdir=''):
    config_name = args.config.split('/')[-1].split('.')[0]
    instance = vrp_instances[args.instance_id]
    return f'{rootdir}/{instance}/{args.agent}/{args.reward}/{args.acceptance}/{config_name}'


def main(args):
    config = configparser.ConfigParser()
    config.read(args.config)
    outdir = output_dir(args, config, rootdir='/mnt/NAS/aldantas/HHRL')
    if os.path.exists(f'{outdir}/{args.run_id}.dat'):
        return
    seed = random.randint(0,10000)
    ProblemClass = autoclass(problem_dict[args.problem])
    problem = ProblemClass(seed)
    problem.loadInstance(args.instance_id)
    # self.problem.setMemorySize(3)
    actions = [0,1,2,3,4,7,8,9]
    state_env = SlidingWindowState(config, actions)
    agent = agent_dict[args.agent](config, actions, state_env=state_env)
    reward = reward_dict[args.reward](config, actions)
    acceptance = acceptance_dict[args.acceptance]()
    hh = HyperHeuristic(problem, agent, reward, acceptance)
    stats = hh.run(args.time_limit)
    stats.run_id = args.run_id
    os.system(f'mkdir -p {outdir}')
    stats.save(outdir)


def parse_args(desc=''):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-p', '--problem', type=str, default='VRP')
    parser.add_argument('-c', '--config', type=str)
    parser.add_argument('-i', '--instance_id', type=int, default=0)
    parser.add_argument('-r', '--run_id', type=int, default=0)
    parser.add_argument('-t', '--time_limit', type=int, default=3)
    parser.add_argument('-ag', '--agent', type=str, default='DQN')
    parser.add_argument('-rw', '--reward', type=str, default='IR')
    parser.add_argument('-ac', '--acceptance', type=str, default='ALL')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
