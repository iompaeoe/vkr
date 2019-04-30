import importlib
import importlib.util

def import_source(module_file_path,module_name):
    ##module_file_path = module_name.__file__
    ##module_name = module_name.__name__
    
    module_spec = importlib.util.spec_from_file_location(
        module_name, module_file_path
    )
    
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)    
    msg = 'The {module_name} module has the following methods: {methods}'
    print(
        msg.format(module_name=module_name, methods=dir(module))
    )
    return module