from py4j.java_gateway import JavaGateway
import configparser
import random
from agent.mab import DMABAgent
from credit import ExtremeValue
from acceptance import AcceptAll
from hh import HyperHeuristic


def main(config):
    hyflex = JavaGateway().jvm
    instance_id = 0
    problem = hyflex.VRP.VRP(random.randint(0,10000))
    problem.loadInstance(instance_id)
    chesc = hyflex.CHeSC(0, 600000, problem)
    # self.problem.setMemorySize(3)
    actions = [0,1,2,3,4,7,8,9]
    agent = DMABAgent(config, actions)
    credit_assignment = ExtremeValue(config, actions)
    acceptance = AcceptAll()

    hh = HyperHeuristic(problem, agent, credit_assignment, acceptance, chesc)
    stats = hh.run()
    stats.save()
    print(stats.best_fitness)
    print(stats.run_time)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(f'configs/default-config.ini')
    main(config)
