from hhrl.util import Loader

if __name__ == "__main__":
    loader = Loader()
    root_dir='results_data_HHRL_states'
    problem_list = ['FS', 'TSP']
    config_list = [('DQN', 'S1'), ('DQNUCB', 'S1')]
    attributes = ['best_fitness']
    results_dict = loader.load_problems(root_dir, problem_list, config_list, attributes, 5)
    print(results_dict)
