import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import csv
from hhrl.util import Loader
from stattests import StatTests


MEDIUM_SIZE = 16


def save_attrs_stat(filename, results_dict, attributes, stat_func):
    if not filename.endswith('.csv'):
        filename = filename + '.csv'
    outfile = open(filename, 'w')
    w = csv.writer(outfile, delimiter=';')
    w.writerow([' ']+attributes)
    for instance_key in results_dict:
        instance_type = instance_key.split('_')[0]
        instance_name = instance_key.split('-')[-1].split('.')[0]
        instance = f'{instance_type}-{instance_name}'
        row = [instance]
        for attr in attributes:
            row.append(stat_func(results_dict[instance_key][attr]))
        w.writerow(row)
    outfile.close()


def get_snapshots(full_trace, n_snapshots=100):
    if n_snapshots > len(full_trace):
        print(f'Number of snapshots {n_snapshots} is higher than the trace length {len(full_trace)}')
        return full_trace
    step = int(len(full_trace) / (n_snapshots))
    snapshots = [full_trace[i] for i in range(0, len(full_trace), step)]
    snapshots[-1] = full_trace[-1]
    return snapshots


def plot_avg_history(instance, instance_dict, attributes):
    for attr in attributes:
        plotdir = f'instance_plots/history/{attr}'
        os.system(f'mkdir -p {plotdir}')
        plt.figure()
        for config in instance_dict:
            history = instance_dict[config][attr]
            avg_history = np.mean(history, 0)
            iterations = range(len(avg_history))
            plt.plot(iterations, avg_history, label=f'{config}', linewidth=.8)
        plt.title(instance)
        plt.xlabel('Iterations')
        plt.ylabel(attr)
        # plt.yticks(np.arange(0, 100, 10))
        # plt.xticks(np.arange(0, max_gen, 10))
        plt.legend(loc='best')
        filepath = f'{plotdir}/{instance}.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()


def make_boxplot(instance, instance_dict, attr='best_fitness'):
    plotdir = f'instance_plots/boxplots'
    os.system(f'mkdir -p {plotdir}')
    plt.figure()
    labels = []
    boxes = []
    for config in instance_dict:
        results = instance_dict[config][attr]
        boxes.append(results)
        labels.append(config)
        # to_trunc = min(map(len, history))
        # avg_history = np.mean([h[:to_trunc] for h in history], 0)
        # iterations = range(len(avg_history))
    plt.boxplot(boxes)
    plt.gca().set_xticklabels(labels, rotation=45, fontsize=8)
    plt.title(instance)
    # plt.xlabel("Iterations")
    # plt.ylabel(attr)
    # plt.yticks(np.arange(0, 100, 10))
    # plt.xticks(np.arange(0, max_gen, 10))
    # plt.legend(loc="best")
    filepath = f'{plotdir}/{instance}.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()


def save_configs_performance(filename, results_dict, attr='best_fitness'):
    if not filename.endswith('.csv'):
        filename = filename + '.csv'
    outfile = open(filename, 'w')
    w = csv.writer(outfile, delimiter=';')
    for instance_key in results_dict:
        configs = []
        for config in sorted(results_dict[instance_key]):
            configs.append(config)
        break
    w.writerow([' ']+ configs)
    for instance_key in results_dict:
        instance_type = instance_key.split('_')[0]
        instance_name = instance_key.split('-')[-1].split('.')[0]
        instance = f'{instance_type}-{instance_name}'
        row = [instance]
        for config in sorted(results_dict[instance_key]):
            results = results_dict[instance_key][config][attr]
            mean = np.around(np.mean(results), 2)
            std = np.around(np.std(results), 2)
            cell = f'{mean} ({std})'
            row.append(cell)
        w.writerow(row)
    outfile.close()


def make_table_n_boxplots(directory, black_list):
    loader = Loader()
    attributes = ['best_fitness']
    results_dict = loader.load(directory, attributes, 4, black_list)
    save_configs_performance('TSP_configs_performance', results_dict, attributes[0])
    for instance in results_dict:
        make_boxplot(instance, results_dict[instance])


def make_history_plots(directory, black_list):
    loader = Loader()
    loader.n_snapshots = 100
    attributes = ['best_fitness_hist']
    for instance, instance_dict in loader.lazy_load(directory, attributes, 4, black_list):
        plot_avg_history(instance, instance_dict, attributes)


def make_hypothesis_test(directory, black_list):
    loader = Loader()
    outdir = 'statistic_plots/'
    stat = StatTests(outdir)
    attributes = ['best_fitness']
    results_dict = loader.load(directory, attributes, 4, black_list, True)
    df = pd.DataFrame.from_dict(results_dict, orient='index')
    experiment_name = 'VRP_TSP_DMAB'
    performance_dict = stat.kruskal_dunn(df, f'{experiment_name}_instance_performance.pdf')
    df = df.applymap(np.mean)
    correct = 'bergmann'
    control = None
    stat.friedman_post(df, f'{experiment_name}_rank_{correct}.pdf', f'{experiment_name}_matrix_{correct}.pdf',
            correct=correct, control=control)
    correct = 'finner'
    control = 'DQN-IR'
    stat.friedman_post(df, f'{experiment_name}_rank_{correct}.pdf', f'{experiment_name}_matrix_{correct}.pdf',
            correct=correct, control=control)
    # for setup in performance_dict:
    #     print(setup)
    #     print(f"better: {len(performance_dict[setup]['better'])}")
    #     print(f"equivalent: {len(performance_dict[setup]['equivalent'])}")
    #     print(f"worse: {len(performance_dict[setup]['worse'])}")


def main():
    directory = 'results'
    black_list = ['DQN', 'FRRMAB', 'BP', 'FS', 'PS', 'SAT']
    # make_table_n_boxplots(directory, black_list)
    # make_history_plots(directory, black_list)
    make_hypothesis_test(directory, black_list)

if __name__ == '__main__':
    main()
