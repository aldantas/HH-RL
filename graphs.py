import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import csv
from hhrl.util import Loader
from stattests import StatTests
from tablemaker import TableMaker


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

def make_label(config, whitelist, split_char='-'):
    config_keys = config.split(split_char)
    allowed_keys = []
    for key in config_keys:
        if key in whitelist:
            allowed_keys


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
    plt.gca().set_xticklabels(labels, fontsize=8)
    # plt.gca().set_xticklabels(labels, rotation=45, fontsize=8)
    # plt.title(instance)
    # plt.xlabel("Iterations")
    # plt.ylabel(attr)
    # plt.yticks(np.arange(0, 100, 10))
    # plt.xticks(np.arange(0, max_gen, 10))
    # plt.legend(loc="best")
    filepath = f'{plotdir}/{instance}.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()


def save_configs_performance(filename, results_dict, performance_dict, file_type='csv'):
    for instance_key in results_dict:
        header = ['Instance']
        for config in sorted(results_dict[instance_key]):
            header.append(config)
        break
    print(header)
    if file_type == 'csv':
        filename = filename + '.csv'
        outfile = open(filename, 'w')
        w = csv.writer(outfile, delimiter=';')
        w.writerow(header)
    elif file_type == 'tex':
        filename = filename + '.tex'
        w = TableMaker(filename, header)
    else:
        print(f'Invalid {file_type} format')
        return
    for instance_key in results_dict:
        instance_type = instance_key.split('-')[0]
        instance_name = instance_key.split('-')[-1]
        instance = f'{instance_type}-{instance_name}'
        row = [instance]
        bold_mask, bg_mask = [False], [False]
        for config in sorted(results_dict[instance_key]):
            if instance_key in performance_dict[config]['equivalent']:
                bold_mask.append(False)
                bg_mask.append(True)
            elif instance_key in performance_dict[config]['better']:
                bold_mask.append(True)
                bg_mask.append(True)
            else:
                bg_mask.append(False)
                bold_mask.append(False)
            results = results_dict[instance_key][config]
            mean = np.around(np.mean(results), 2)
            std = np.around(np.std(results), 2)
            cell = f'{mean} ({std})'
            row.append(cell)
        print(len(row), len(bold_mask), len(bg_mask))
        w.writerow(row, bold_mask, bg_mask)
    if file_type == 'csv':
        outfile.close()
    elif file_type == 'tex':
        w.save('Table')


def make_boxplots(directory, black_list, key_whitelist):
    loader = Loader()
    attributes = ['best_fitness']
    results_dict = loader.load(directory, attributes, 4, black_list, key_whitelist)
    for instance in results_dict:
        make_boxplot(instance, results_dict[instance])


def make_history_plots(directory, black_list):
    loader = Loader()
    loader.n_snapshots = 100
    attributes = ['best_fitness_hist']
    for instance, instance_dict in loader.lazy_load(directory, attributes, 4, black_list):
        plot_avg_history(instance, instance_dict, attributes)


def make_hypothesis_test(directory, black_list, key_whitelist):
    loader = Loader()
    outdir = 'statistic_plots/'
    stat = StatTests(outdir)
    attributes = ['best_fitness']
    results_dict = loader.load(directory, attributes, 4, black_list, key_whitelist, True)
    df = pd.DataFrame.from_dict(results_dict, orient='index')
    experiment_name = 'TSP_VRP_DQN_DMAB_FRRMAB'
    performance_dict = stat.kruskal_dunn(df, f'{experiment_name}_instance_performance.pdf')
    df = df.applymap(np.mean)
    correct = 'bergmann'
    control = None
    stat.friedman_post(df, f'{experiment_name}_rank_{correct}.pdf', f'{experiment_name}_matrix_{correct}.pdf',
            correct=correct, control=control)
    correct = 'finner'
    control = 'DQN'
    stat.friedman_post(df, f'{experiment_name}_rank_{correct}.pdf', f'{experiment_name}_matrix_{correct}.pdf',
            correct=correct, control=control)
    save_configs_performance('VRP_TSP_configs_performance', results_dict, performance_dict, 'tex')


def main():
    directory = 'results'
    black_list = ['BP', 'FS', 'PS', 'SAT', 'EV', 'rank_decay_05']
    key_whitelist = ['DQN', 'DMAB', 'FRRMAB']
    # make_boxplots(directory, black_list, key_whitelist)
    # make_history_plots(directory, black_list)
    make_hypothesis_test(directory, black_list, key_whitelist)

if __name__ == '__main__':
    main()
