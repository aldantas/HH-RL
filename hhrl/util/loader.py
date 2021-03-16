import os
import pickle
import numpy as np
from tqdm import tqdm
from hhrl.util import StatsInfo


class Loader:
    def __init__(self):
        self.loaded_attributes = tuple()

    def read_file_attrs(self, file_path, load_attrs):
        try:
            result = pickle.load(open(file_path, 'rb'))
        except Exception as e:
            print(file_path)
            raise e
        for attr_str in load_attrs:
            attr = getattr(result, attr_str)
            yield attr_str, attr

    def read_dir(self, dir_path, load_attrs, pbar=False):
        dir_dict = {}
        iter_dir = os.listdir(dir_path)
        if pbar:
            iter_dir = tqdm(iter_dir)
        for child in iter_dir:
            child_path = f'{dir_path}/{child}'
            if os.path.isfile(child_path):
                for attr_str, attr_value in self.read_file_attrs(child_path, load_attrs):
                    dir_dict.setdefault(attr_str,[]).append(attr_value)
            else:
                dir_dict[child] = self.read_dir(child_path, load_attrs)
        return dir_dict

    def load_results(self, results_dir, attributes, configs=(), flatten_key=True, pbar=True):
        results_dict = self.read_dir(results_dir, attributes, pbar=pbar)
        if flatten_key:
            results_dict = self.__flatten_dict(results_dict, attributes, configs)
        self.loaded_attributes = tuple(attributes)
        return results_dict

    def __tuple_to_flat_key(self, keys_tuple):
        flat_key = ''
        for key in keys_tuple:
            flat_key += f'-{key}'
        return flat_key.lstrip('-')

    def __flatten_dict(self, nested_dict, attributes, configs=(), keys_tuple=()):
        flat_dict = {}
        for key in nested_dict:
            if isinstance(nested_dict[key], dict):
                # key_list.append(key)
                # new_key = f'{flat_key}-{key}'
                new_tuple = keys_tuple + (key,)
                new_dict = self.__flatten_dict(
                        nested_dict[key], attributes, configs, new_tuple)
                if len(new_dict) == 0:
                    continue
                flat_key = list(new_dict.keys())[0]
                if flat_key in flat_dict:
                    flat_dict[flat_key].update(new_dict[flat_key])
                else:
                    flat_dict.update(new_dict)
            elif key in attributes:
                # flat_key = flat_key.lstrip('-')
                if keys_tuple[-1] in configs:
                    flat_key = self.__tuple_to_flat_key(keys_tuple[:-1])
                    config_key = keys_tuple[-1]
                    return {flat_key: {config_key: {key: nested_dict[key]}}}
                else:
                    # flat_key = self.__tuple_to_flat_key(keys_tuple)
                    # return {flat_key: {key: nested_dict[key]}}
                    return {}
        return flat_dict

    def get_dataframe(self, results_ditct, attribute):
        if attribute not in self.loaded_attributes:
            return
        df_dict = {}
        for instance in self.results_dict:
            df_dict[instance] = self.__flatten_dict(results_dict[instance], attribute)
