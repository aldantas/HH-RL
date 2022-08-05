import numpy as np
from hhrl.util import Loader


problems = ['SAT', 'BP', 'PS', 'FS', 'TSP', 'VRP']

tsp_mapping = {
        0: 'TSP-pr299',
        1: 'TSP-usa13509',
        2: 'TSP-rat575',
        3: 'TSP-u2152',
        4: 'TSP-d1291'
        }


sat_mapping = {
        0: 'SAT-instance_n3_i3_pp',
        1: 'SAT-instance_n3_i4_pp_ci_ce',
        2: 'SAT-instance_n3_i3_pp_ci_ce',
        3: 'SAT-id_10',
        4: 'SAT-id_11'
        }


fs_mapping = {
        0: 'FS-100x20-2',
        1: 'FS-500x20-2',
        2: 'FS-100x20-4',
        3: 'FS-id_10',
        4: 'FS-id_11'
        }


# def get_alg_results(results_list, i):
#     alg_dict = {}
#     for instance in range(1, 6):
#         alg_dict[instance] = {}
#         i += 1
#         j = i+1
#         alg_dict[instance]['median'] = results_list[i]
#         alg_dict[instance]['min'] = results_list[j]
#     return alg_dict


# with open('chesc_results.txt') as chesc_file:
#     results_list = [line.rstrip('\n') for line in chesc_file.readlines()]


# chesc_dict = {}
# i = 0
# while i < len(results_list):
#     item = results_list[i]
#     i += 1
#     if item in problems:
#         problem = item
#         chesc_dict[problem] = {}
#     elif not item.isnumeric():
#         alg = item
#         chesc_dict[problem][alg] = get_alg_results(results_list, i)
#         i += 10

def load_chesch(filepath):
    algs_dict = {}
    for line in open(filepath):
        line = line.lstrip().rstrip('\n').split('\t')
        algs_dict[line[0]] = [float(value) for value in line[1:]]
    return algs_dict

loader = Loader()
input_dir = 'results_data_HHRL_states/'
attributes = ['best_fitness']
key_whitelist = ['DQN', 'BOLLP', 'SW']
problems = {'TSP': ['tsp_chesc.txt', tsp_mapping], 'SAT': ['sat_chesc.txt', sat_mapping],
        'FS': ['fs_chesc.txt', fs_mapping]}
ignore_configs = ['FRRMAB', 'BP', 'PS', 'VRP']

for problem in problems:
    black_list = list(problems.keys()) + ignore_configs
    black_list.remove(problem)
    results_dict = loader.load(input_dir, attributes, 5, black_list, key_whitelist, True)
    print(f'{problem},,')
    print('Instance, AdapHH, DQN-BOLLP, DQN-SW')
    chesc_filepath, mapping = problems[problem]
    algs_dict = load_chesch(chesc_filepath)
    for instance in mapping:
        adaphh_median = algs_dict['AdapHH'][instance]
        dqn_bollp_median = np.median(results_dict[mapping[instance]]['DQN-BOLLP'])
        dqn_sw_median = np.median(results_dict[mapping[instance]]['DQN-SW'])
        print(f'{instance}, {adaphh_median},  {dqn_bollp_median}, {dqn_sw_median}')
