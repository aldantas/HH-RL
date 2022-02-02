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
        snapshots = [full_trace[i] for i in np.linspace(0, len(full_trace) - 1, self.n_snapshots, dtype=int)]
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

    def _allow_instance_path(self, path, instance_list):
        if not instance_list:
            return True
        return any([
            True if instance in path.parts else False for instance in instance_list
        ])

    def _allow_config_path(self, path, config_list):
        if not config_list:
            return True
        return any([
            all([
                True if config_key in path.parts else False for config_key in config_tuple
            ]) for config_tuple in config_list
        ])

    def get_paths_dict(self, root_dir, instance_list, config_list, split_depth):
        paths_dict = {}
        for root, dirs, files in os.walk(root_dir):
            if not dirs:
                path = pathlib.Path(root)
                instance_path = pathlib.Path(*path.parts[:-split_depth])
                if not self._allow_instance_path(instance_path, instance_list):
                    continue
                config_path = pathlib.Path(*path.parts[-split_depth:])
                if self._allow_config_path(config_path, config_list):
                    paths_dict.setdefault(instance_path, []).append(config_path)
        return paths_dict

    def __is_black_listed(self, path, black_list):
        for item in black_list:
            if item in str(path):
                return True
        return False

    def __tuple_to_str_key(self, keys_tuple, key_whitelist=None):
        str_key = ''
        if key_whitelist is None:
            key_whitelist = keys_tuple
        for key in keys_tuple:
            if key in key_whitelist:
                str_key += f'-{key}'
        return str_key.lstrip('-')

    def lazy_load(self, directory, attributes, split_depth=1, black_list=[], key_whitelist=None,
                  use_attr_list=False):
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
                # TODO: parameterize the config_key slicing
                # config_key = self.__tuple_to_str_key(config_path.parts[:2])
                config_key = self.__tuple_to_str_key(config_path.parts, key_whitelist)
                if use_attr_list:
                    instance_dict[config_key] = []
                else:
                    instance_dict[config_key] = {}
                for file in tqdm(os.listdir(path), leave=False):
                    for attr_str, attr_value in self.read_file_attrs(path / file, attributes):
                        if use_attr_list:
                            instance_dict[config_key].append(attr_value)
                        else:
                            instance_dict[config_key].setdefault(attr_str, []).append(attr_value)
            yield instance_key, instance_dict

    def __get_config_index(self, path_parts, config_list):
        for i, config_parts in enumerate(config_list):
            if set(path_parts).issuperset(set(config_parts)):
                return i
        return None

    def lazy_load_instances(self, root_dir, config_list, attribute_list, instance_list, config_keys=[],
            split_depth=1, use_attr_list=False):
        paths_dict = self.get_paths_dict(root_dir, instance_list, config_list, split_depth)
        for instance_path in tqdm(paths_dict):
            instance_key = self.__tuple_to_str_key(instance_path.parts[1:])
            instance_dict = {}
            for config_path in tqdm(paths_dict[instance_path], leave=False):
                path = instance_path / config_path
                # TODO: parameterize the config_key slicing
                # config_key = self.__tuple_to_str_key(config_path.parts[:2])

                if config_keys:
                    config_idx = self.__get_config_index(config_path.parts, config_list)
                    config_key = config_keys[config_idx]
                else:
                    config_key = self.__tuple_to_str_key(config_path.parts)

                if use_attr_list:
                    instance_dict[config_key] = []
                else:
                    instance_dict[config_key] = {}

                for file in tqdm(os.listdir(path), leave=False):
                    for attr_str, attr_value in self.read_file_attrs(path / file, attribute_list):
                        if use_attr_list:
                            instance_dict[config_key].append(attr_value)
                        else:
                            instance_dict[config_key].setdefault(attr_str, []).append(attr_value)
            yield instance_key, instance_dict

    def load(self, directory, attributes, split_depth=1, black_list=[], key_whitelist=None,
             use_attr_list=False):
        results_dict = {}
        for instance_key, instance_dict in self.lazy_load(
                directory, attributes, split_depth, black_list, key_whitelist, use_attr_list):
            results_dict[instance_key] = instance_dict
        return results_dict

    def check_experiments(self, root_dir, split_depth=5):
        experiemnts_dict = {}
        for problem in os.listdir(root_dir):
            print(problem)
            problem_dir = f'{root_dir}/{problem}'
            paths_dict = self.get_paths_dict(problem_dir, None, None, split_depth=split_depth)
            experiemnts_dict[problem] = {}
            problem_configs = []
            for instance_path in paths_dict:
                instance_dict = {}
                for config_path in paths_dict[instance_path]:
                    full_path = f'{instance_path}/{config_path}'
                    count = len(os.listdir(full_path))
                    problem_configs.append((full_path, count))
            problem_configs.sort()
            for config in problem_configs:
                if config[1] != 31:
                    print(config)


    def load_problems(self, root_dir, problem_list, config_list, attribute_list, instance_list=None,
            config_keys=[], split_depth=1, use_attr_list=False):
        results_dict = {}
        for problem in problem_list:
            problem_dir = f'{root_dir}/{problem}'
            problem_dict = {}
            for instance_key, instance_dict in self.lazy_load_instances(
                    problem_dir, config_list, attribute_list, instance_list, config_keys, split_depth, use_attr_list):
                if len(instance_dict.values()) < len(config_list):
                    continue
                problem_dict[instance_key] = instance_dict
            yield problem, problem_dict
