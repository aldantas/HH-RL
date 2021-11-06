import pickle
import csv
import os


class StatsInfo:
    def __init__(self, initial_fitness):
        self.fitness_hist = []
        self.best_fitness_hist = []
        self.heuristic_hist = []
        self.reward_hist = []
        self.best_solution = None
        self.run_id = 0
        self.run_time = 0.0
        self.initial_fitness = initial_fitness
        self.best_fitness = None
        self.iterations = 0
        self.state_hist = []

    def __str__(self):
        return str(self.best_fitness)

    def push_heuristic(self, heuristic, reward, state=None):
        self.heuristic_hist.append(heuristic)
        self.reward_hist.append(reward)
        if state:
            self.state_hist.append(state)

    def push_fitness(self, current, best):
        self.fitness_hist.append(current)
        self.best_fitness_hist.append(best)

    def save(self, outdir='.', save_csv=False):
        filepath = f'{outdir}/{self.run_id}.dat'
        pickle.dump(self, open(filepath, 'wb'))
        if save_csv:
            self.save_csv(outdir)

    def save_csv(self, outdir='.'):
        filename = 'fitness_history'
        history = self.best_fitness_hist
        initial = self.initial_fitness
        open_flag = 'w'
        if os.path.isfile(f'{outdir}/{filename}.csv'):
            open_flag = 'a'
        with open(f'{outdir}/{filename}.csv', open_flag, newline='') as evol_file:
            w = csv.writer(evol_file, delimiter=';')
            if open_flag == 'w':
                w.writerow(('run', 'iter', 'fitness'))
                w.writerow((self.run_id, 0, initial))
            for it, fitness in enumerate(history):
                line = (self.run_id, it+1, fitness)
                w.writerow(line)
