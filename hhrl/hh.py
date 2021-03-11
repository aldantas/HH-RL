import time
from hhrl.util.stats_info import StatsInfo


class HyperHeuristic:
    def __init__(self, problem, agent, credit_assignment, acceptance, chesc=None):
        self.problem = problem
        self.chesc = chesc
        self.agent = agent
        self.credit_assignment = credit_assignment
        self.acceptance = acceptance

    def initiallize_time(self):
        if self.chesc is not None:
            self.chesc.startTimer()
        self.start_time = time.process_time()

    def elapsed_time(self):
        python_elapsed = time.process_time() - self.start_time
        if self.chesc is not None:
            java_elapsed = self.chesc.getElapsedTime()
            return python_elapsed + java_elapsed
        return python_elapsed

    def run(self, time_limit=3000):
        self.problem.initialiseSolution(0)
        current_fitness = self.problem.getFunctionValue(0)
        iterations = 0
        stats = StatsInfo(current_fitness)
        stats.push_fitness(current_fitness, current_fitness)
        self.initiallize_time()
        while self.elapsed_time() < time_limit:
            llh = self.agent.select()
            fitness = self.problem.applyHeuristic(llh, 0, 1)
            delta = current_fitness - fitness
            reward = self.credit_assignment.get_reward(llh, fitness, current_fitness)
            if self.acceptance.is_solution_accepted(delta):
                self.problem.copySolution(1, 0)
                current_fitness = fitness
            self.agent.update(reward, llh)
            stats.push_fitness(current_fitness, self.problem.getBestSolutionValue())
            iterations += 1
        stats.best_fitness = self.problem.getBestSolutionValue()
        stats.run_time = self.elapsed_time()
        stats.iterations = iterations
        return stats
