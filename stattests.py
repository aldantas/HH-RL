from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
import rpy2.robjects.numpy2ri as rnp
import rpy2.robjects as ro
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
plt.style.use('ggplot')

rnp.activate()
scmamp = importr('scmamp')
pmcmr = importr('PMCMRplus')
grdevices = importr('grDevices')
ro.r('''
    library('ggplot2')
    plotpv <- function(pvmatrix, filename) {
        plot <- plotPvalues(pvmatrix)
        plot + labs(title="Corrected p-values using Bergmann and Hommel procedure") +
        scale_fill_gradientn("Corrected p-values", colours=c("skyblue4", "orange"))
        ggsave(filename, width=300, unit='mm')
    }
    ''')

class StatTests:
    image_devices = {
            'jpeg': grdevices.jpeg,
            'jpg': grdevices.jpeg,
            'png': grdevices.png,
            'pdf': grdevices.pdf,
            'ps': grdevices.postscript,
            'postscript': grdevices.postscript
            }

    def __init__(self, output_location='.'):
        self.output_location = output_location
        os.system(f'mkdir -p {output_location}')

    def __open_plot_file(self, filename):
        extension = filename.split('.')[-1]
        filedriver = self.image_devices.get(extension, grdevices.pdf)
        filedriver(f'{self.output_location}/{filename}')

    def __close_plot_file(self):
        grdevices.dev_off()

    def __convert_df(self, df):
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_df = ro.conversion.py2rpy(df)
        return r_df

    # def friedman_post_bergmanhommel(self, df, filename, control=None):
    #     print('Friedman with BergmanHommel PostHoc')
    #     r_df = self.__convert_df(df)
    #     friedman = scmamp.friedmanTest(r_df)
    #     print(friedman)
    #     if not control:
    #         control = ro.r('NULL')
    #     pv_matrix = scmamp.friedmanPost(r_df, control=control)
    #     adjusted_pv = scmamp.adjustBergmannHommel(pv_matrix)
    #     ro.r['plotpv'](adjusted_pv, filename)

    def friedman_post(self, df, rank_filename, matrix_filename, correct='bergmann', control=None):
        print(f'Friedman with {correct} PostHoc')
        # This is needed because the postHocTest method ranks according to the highest values (maximization
        # problems)
        df = df *-1
        r_df = self.__convert_df(df)
        if not control:
            control = ro.r('NULL')
        friedman = scmamp.friedmanTest(r_df)
        pvalue = friedman.rx2('p.value')[0]
        print(f'Friedman p-value: {pvalue}')
        if len(df.columns) <= 2:
            return
        ro.r('''
            f <- function(df, rank_filepath, matrix_filepath, correct, control) {
                post.results <- postHocTest(data=df, test="friedman", correct=correct, control=control,
                use.rank=TRUE)
                pdf(rank_filepath)
                plotRanking(post.results$corrected.pval, post.results$summary, decreasing=FALSE)
                dev.off()
                alg.order <- order(post.results$summary)
                plot <- plotPvalues(post.results$corrected.pval, alg.order=alg.order)
                plot + labs(title="Corrected p-values")
                # scale_fill_gradientn("Corrected p-values", colours=c("skyblue4", "orange"))
                ggsave(matrix_filepath, width=500, unit='mm')
                return(post.results)
            }
                '''
            )
        rank_filepath = f'{self.output_location}/{rank_filename}'
        matrix_filepath = f'{self.output_location}/{matrix_filename}'
        print(control)
        results = ro.r['f'](r_df, rank_filepath, matrix_filepath, correct, control)
        print(results)

    def friedman_post_nemenyi(self, df, filename, control=None):
        print('Friedman with Nemenyi PostHoc')
        r_df = self.__convert_df(df)
        friedman = scmamp.friedmanTest(r_df)
        print(friedman)
        if len(df.columns) <= 2:
            return
        posthoc = scmamp.nemenyiTest(r_df, alpha=0.05)
        print(posthoc)
        self.__open_plot_file(filename)
        plot = scmamp.plotCD(r_df, alpha=0.05, decreasing=False)
        self.__close_plot_file()

    def kruskal_dunn(self, df, filename=None):
        algs = df.columns.tolist()
        algs_performance_dict = {}
        for alg in algs:
            algs_performance_dict[alg] = {'better': [], 'equivalent': [], 'worse': []}
        for idx, row in df.iterrows():
            instance = row.name
            data_sample = row.tolist()
            if np.min(data_sample) == np.max(data_sample):
                for alg in algs:
                    algs_performance_dict[alg]['equivalent'].append(instance)
                continue
            means = np.mean(data_sample, 1)
            rank_order = means.argsort()
            # reorders the algs list and data_sample according to the mean performance
            sorted_algs = [algs[i] for i in rank_order]
            data_sample = [data_sample[i] for i in rank_order]
            means.sort()
            kruskal = pmcmr.kruskalTest(data_sample)
            pvalues = kruskal.rx2('p.value')
            if pvalues[0] > 0.05:
                for alg in algs:
                    algs_performance_dict[alg]['equivalent'].append(instance)
                continue
            if len(df.columns) > 2:
                post_test = pmcmr.kwManyOneDunnTest(data_sample, p_adjust_method='holm')
                pvalues = post_test.rx2('p.value')
            has_equivalent = False
            # for p, alg, mean in zip(post_test[2], sorted_algs[1:], means[1:]):
            for p, alg, mean in zip(pvalues, sorted_algs[1:], means[1:]):
                if p > 0.05:
                    algs_performance_dict[alg]['equivalent'].append(instance)
                    has_equivalent = True
                else:
                    algs_performance_dict[alg]['worse'].append(instance)
            best_alg = sorted_algs[0]
            if has_equivalent:
                algs_performance_dict[best_alg]['equivalent'].append(instance)
            else:
                algs_performance_dict[best_alg]['better'].append(instance)
        if filename:
            self.plot_performance_bars(algs_performance_dict, filename, 'Instance Performance')
        return algs_performance_dict

    def __label_bar(self, bar, color, offset=0):
        height = bar.get_height()
        if height > 0:
            plt.gca().text(bar.get_x() + bar.get_width()/2., height+offset-.15,
                    '%d' % int(height),
                    ha='center', va='bottom', color=color)

    def plot_performance_bars(self, performance_dict, filename, title):
        labels = []
        better_count = []
        equivalent_count = []
        for alg in performance_dict:
            if alg == 'DQN-RIP':
                label = r'$R_{1}$'
            elif alg == 'DQN-IR':
                label = r'$R_{2}$'
            else:
                label = alg
            labels.append(label)
            better_count.append(len(performance_dict[alg]['better']))
            equivalent_count.append(len(performance_dict[alg]['equivalent']))
        labels.reverse()
        better_count.reverse()
        equivalent_count.reverse()
        width = .8
        plt.figure()
        bottom_bars = plt.bar(labels, better_count, width, label='Better', color='black')
        upper_bars = plt.bar(labels, equivalent_count, width, bottom=better_count, label='Equivalent', color='gray')
        for bbar, ubar in zip(bottom_bars, upper_bars):
            self.__label_bar(bbar, 'white')
            offset = bbar.get_height()
            self.__label_bar(ubar, 'black', offset)
        plt.xticks(rotation=45)
        plt.ylabel('Instances')
        plt.title(title)
        plt.legend()
        plt.savefig(f'{self.output_location}/{filename}', dpi=300, bbox_inches='tight')
        # plt.show()
        plt.close()
