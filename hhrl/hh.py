import time
from hhrl.util.stats_info import StatsInfo


class HyperHeuristic:
    def __init__(self, problem, agent, credit_assignment, acceptance):
        self.problem = problem
        self.agent = agent
        self.credit_assignment = credit_assignment
        self.acceptance = acceptance

    def __elapsed_time(self):
        self.elapsed = time.process_time() - self.start_time
        return self.elapsed

    def run(self, time_limit=3):
        self.problem.initialise_solution()
        current_fitness = self.problem.get_fitness()
        iterations = 0
        stats = StatsInfo(current_fitness)
        stats.push_fitness(current_fitness, current_fitness)
        self.start_time = time.process_time()
        while self.__elapsed_time() < time_limit:
            llh = self.agent.select()
            fitness = self.problem.apply_heuristic(llh)
            # solution = self.problem.get_solution()
            delta = current_fitness - fitness
            reward = self.credit_assignment.get_reward(llh, fitness, current_fitness)
            if self.acceptance.is_solution_accepted(delta):
                self.problem.accept_solution()
                current_fitness = fitness
            self.agent.update(action=llh, reward=reward, solution=self.problem.get_solution(),
                    elapsed=self.elapsed)
            stats.push_fitness(current_fitness, self.problem.get_best_fitness())
            stats.push_heuristic(llh, reward, self.agent.get_env_state())
            iterations += 1
        stats.best_fitness = self.problem.get_best_fitness()
        stats.run_time = self.elapsed
        stats.iterations = iterations
        return stats
