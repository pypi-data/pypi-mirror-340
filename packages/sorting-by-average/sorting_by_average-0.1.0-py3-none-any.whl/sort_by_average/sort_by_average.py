import numpy as np
from typing import List, Union, Tuple
import sys

from sort_by_average.call_func import call_func

class SortByAverage:
    """
    Class to sort an array of integers, dictionaries, or tuples by averaging values.
    Supports custom external function calls for additional processing.
    """
    
    def __init__(
        self, 
        arr: Union[List[int], List[dict], Tuple], 
        step: int = 2, 
        module_name: str = None, 
        function_name: str = None, 
        is_desc: bool = False, 
        is_index: bool = False, 
        is_i_called: bool = False,
        set_recursion_limit: int = None,
        **kwargs
    ):
        """
        Initializes the SortByAverage class.

        :param arr: Input data (list of integers, dictionaries, or tuples)
        :param step: Step size for sorting process
        :param module_name: External module name for function call
        :param function_name: External function name to be called
        :param is_desc: Sort order (descending if True)
        :param is_index: Return indexes instead of values
        :param is_i_called: Pass iteration count to external function if True
        :param set_recursion_limit: Optional recursion limit to avoid stack overflow
        :param kwargs: Additional keyword arguments
        """

        self.arr = arr
        self.original_data = arr
        self.step = step
        self.module_name = module_name
        self.function_name = function_name
        self.is_desc = is_desc
        self.is_index = is_index
        self.is_i_called = is_i_called
        self.kwargs = kwargs
        
        self.used_indexes = {}
        self.index_map = {}
        
        if set_recursion_limit:
            sys.setrecursionlimit(set_recursion_limit)
            
        #Check if arr is not empty
        try:
            if not arr:
                raise AttributeError("Missing data to sort.")
        except Exception as e:
           raise AttributeError("Missing data to sort.")
                
        #I variant - list, the rest is obvious
        if isinstance(arr[0], int):
            self.arr = np.array(arr, dtype=np.int32)
            self._prepare_index_map_for_list()
        elif isinstance(arr[0], dict):
            self._prepare_index_map_for_dict()
        elif isinstance(arr[0], tuple):
            self._prepare_index_map_for_tuple()
        else:
            raise TypeError("Unsupported data type in input array.")
        
        self._format_step()
        
    def _prepare_index_map_for_list(self):
        """Prepares index mapping for list of integers."""
        self.index_map = {value: set() for value in self.arr}
        for idx, value in enumerate(self.arr):
            self.index_map[value].add(idx)
        return

    def _prepare_index_map_for_dict(self):
        """Prepares index mapping for list of dictionaries."""
        value_key = self.kwargs.get("dict_key_value")
        if not value_key:
            raise KeyError("No passed key to reach value from dict.")
        
        index_key = self.kwargs.get("dict_key_index")
        if not index_key:
            raise KeyError("No passed key to reach index from dict.")
        
        arr = []
        for element in self.arr:
            value = element.get(value_key)
            if value is None:
                raise KeyError("Wrong key to find value passed.")
            try:
                self.index_map.setdefault(value, set()).add(element[index_key])
            except KeyError:
                raise KeyError("Wrong index key passed in dict - no int value")
            arr.append(value)
        self.arr = np.array(arr, dtype=np.int32)
        return

    def _prepare_index_map_for_tuple(self):
        """Prepares index mapping for list of tuples."""
        index_key = self.kwargs.get("tuple_key_index", 0)
        value_key = self.kwargs.get("tuple_key_value", 1)
        arr = []
        for element in self.arr:
            value = element[value_key]
            index = element[index_key]
            self.index_map.setdefault(value, set()).add(index)
            arr.append(value)
        self.arr = np.array(arr, dtype=np.int32)
        return

    def _format_step(self):
        """Adjusts step size to 10% of array length, with a minimum value of 2."""
        self.step = max(4, int(len(self.arr) * 0.1))
        return

    def _process_and_sort_array(self, current_array, i):
        """Processes and sorts a sub-array, optionally calling an external function."""
        before_exec = current_array.copy()

        if self.module_name and self.function_name:
            try:
                if self.is_i_called:
                    current_array = call_func(self.module_name, self.function_name, current_array.tolist(), kwargs = {"i" : i})
                else:
                    current_array = call_func(self.module_name, self.function_name, current_array.tolist())
            except Exception as e:
                raise RuntimeError(f"Error calling external function: {e}")

        arr_to_sort = []
        for original, processed in zip(before_exec, current_array):
            indexes = self.index_map[original]
            used_index = next((idx for idx in indexes if idx not in self.used_indexes.get(original, set())), next(iter(indexes)))
            self.used_indexes.setdefault(original, set()).add(used_index)
            arr_to_sort.append((used_index, processed))

        structured_array = np.array(arr_to_sort, dtype=[('index', 'i4'), ('value', 'i4')])
        sorted_data = np.sort(structured_array, order='value')

        return sorted_data

    def get_original_data_from_dict(self):
        """Additional method when list of dict passed to class as arr. By knowing sequence of values dicts are ordered.
        """
        try:
            new_value_key_name = self.kwargs.get("new_value_key_name", None)
            if not isinstance(self.original_data[0], dict):
                raise AttributeError("Method bookend only with passing list of dicts.")
            if not new_value_key_name:
                new_value_key_name = "calculated_value"

            data_dict = {d[self.kwargs.get("dict_key_index")]: d for d in self.original_data}
            return [{**data_dict[element[0]], new_value_key_name: element[1]} for element in self.sorted_list]
        except TypeError:
            print("Cannot do this method until data is sorted without index.")
            
    def sort(self):
        """Main sorting function based on averaging logic."""
        stack = [(0, len(self.arr))]
        result = []
        i = 0
        
        while stack:
            start, end = stack.pop()
            current_array = self.arr[start:end]
            
            if len(current_array) <= self.step:
                sorted_data = self._process_and_sort_array(current_array, i)
                result.append(sorted_data)
                continue
            
            avg_normalized = np.mean(current_array)
            below_average = current_array[current_array < avg_normalized]
            above_or_equal_average = current_array[current_array >= avg_normalized]

            stack.append((start + len(below_average), end))
            stack.append((start, start + len(below_average)))

            self.arr[start:start + len(below_average)] = below_average
            self.arr[start + len(below_average):end] = above_or_equal_average
            i += 1

        combined_array = np.concatenate(result)
        
        if self.is_desc:
            combined_array = combined_array[::-1]

        if self.is_index:
            sorted_list = [(int(item['index']), int(item['value'])) for item in combined_array]
        else:
            sorted_list = [int(item['value']) for item in combined_array]
        
        self.sorted_list = sorted_list

        return sorted_list
