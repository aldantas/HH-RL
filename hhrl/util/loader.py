import os
import pickle
import numpy as np
import pathlib
from tqdm import tqdm
from hhrl.util import StatsInfo


class Loader:
    def __init__(self):
        self.n_snapshots = 0

    def get_snapshots(self, full_trace):
        if self.n_snapshots > len(full_trace):
            print(f'Number of snapshots {self.n_snapshots} is higher than the trace length {len(full_trace)}')
            return full_trace
        snapshots = [full_trace[i] for i in np.linspace(0, len(full_trace)-1, self.n_snapshots, dtype=int)]
        return snapshots

    def read_file_attrs(self, file_path, load_attrs):
        try:
            result = pickle.load(open(file_path, 'rb'))
        except Exception as e:
            print(file_path)
            raise e
        for attr_str in load_attrs:
            attr = getattr(result, attr_str)
            if isinstance(attr, list) and self.n_snapshots > 0:
                attr = self.get_snapshots(attr)
            yield attr_str, attr

    def get_paths_dict(self, directory, split_depth):
        paths_dict = {}
        for root, dirs, files in os.walk(directory):
            if not dirs:
                path = pathlib.Path(root)
                instance_path = pathlib.Path(*path.parts[:-split_depth])
                config_path = pathlib.Path(*path.parts[-split_depth:])
                paths_dict.setdefault(instance_path,[]).append(config_path)
        return paths_dict

    def __is_black_listed(self, path, black_list):
        for item in black_list:
            if item in str(path):
                return True
        return False

    def __tuple_to_str_key(self, keys_tuple):
        str_key = ''
        for key in keys_tuple:
            str_key += f'-{key}'
        return str_key.lstrip('-')

    def lazy_load(self, directory, attributes, split_depth=1, black_list=[]):
        paths_dict = self.get_paths_dict(directory, split_depth)
        for instance_path in tqdm(paths_dict):
            if self.__is_black_listed(instance_path, black_list):
                continue
            instance_key = self.__tuple_to_str_key(instance_path.parts[1:])
            instance_dict = {}
            for config_path in tqdm(paths_dict[instance_path], leave=False):
                if self.__is_black_listed(config_path, black_list):
                    continue
                path = instance_path / config_path
                config_key = self.__tuple_to_str_key(config_path.parts)
                instance_dict[config_key] = {}
                for file in tqdm(os.listdir(path), leave=False):
                    for attr_str, attr_value in self.read_file_attrs(path/file, attributes):
                        instance_dict[config_key].setdefault(attr_str,[]).append(attr_value)
            yield instance_key, instance_dict

    def load(self, directory, attributes, split_depth=1, black_list=[]):
        results_dict = {}
        for instance_key, instance_dict in self.lazy_load(directory, attributes, split_depth, black_list):
            results_dict[instance_key] = instance_dict
        return results_dict
