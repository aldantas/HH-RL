from py4j.java_gateway import JavaGateway
import configparser
import random
import argparse
import csv
from hhrl.agent.mab import DMABAgent, FRRMABAgent
from hhrl.agent.rl import DQNAgent
from hhrl.reward import ExtremeValue, ImprovementRate
from hhrl.state import SlidingWindowState
from hhrl.acceptance import AcceptAll
from hhrl.hh import HyperHeuristic


def main(args, config):
    hyflex = JavaGateway().jvm
    seed = random.randint(0,10000)
    problem = eval('hyflex.' + get_problem(args.problem))
    problem.loadInstance(args.instance_id)
    chesc = hyflex.CHeSC(0, 600000, problem)
    # self.problem.setMemorySize(3)
    actions = [0,1,2,3,4,7,8,9]
    state_env = SlidingWindowState(config, actions)
    agent = DQNAgent(config, actions, state_env=state_env)
    reward = ImprovementRate(config, actions)
    acceptance = AcceptAll()

    hh = HyperHeuristic(problem, agent, reward, acceptance, chesc)
    stats = hh.run()
    stats.save()
    print(stats.best_fitness)
    print(stats.run_time)


def get_problem(problem):
    problem_dict = {}
    reader = csv.DictReader(open(f'configs/problems.csv'), delimiter=';')
    for row in reader:
        if row['problem'] == problem:
            return row['call']


def parse_args(desc=''):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-p', '--problem', type=str, default='VRP')
    parser.add_argument('-i', '--instance_id', type=int, default=0)
    parser.add_argument('-r', '--run_id', type=int, default=0)
    return parser.parse_args()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(f'configs/default-config.ini')
    args = parse_args()
    main(args, config)
