import importlib
import importlib.util
import os

def call_func(module_name:str, function_name:str, args = None, kwargs = None):

    if module_name.endswith(".py"):
        module_path = os.path.abspath(module_name)
        module_name = os.path.basename(module_path).replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        module = importlib.import_module(module_name)
    
    dynamic_function = getattr(module, function_name)

    if isinstance(args, dict):
        kwargs = args
        args = None
    
    args = args or []
    kwargs = kwargs or {}
    
    return dynamic_function(*args, **kwargs)