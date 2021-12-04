import os
from hhrl.util import Loader

l = Loader()
l.check_experiments('results_data_HHRL_states/')

# for line in open('temp.txt'):
#     # cur_dir = '/home/aldantas/github/HH-RL'
#     parts = line.rstrip('\n').split('/')[:-3]
#     input_dir = '/'.join(parts)
#     parts[-1] = 'SW'
#     output_dir = '/'.join(parts)
#     print(input_dir)
#     print(output_dir)
#     os.system(f'mv {input_dir} {output_dir}')
