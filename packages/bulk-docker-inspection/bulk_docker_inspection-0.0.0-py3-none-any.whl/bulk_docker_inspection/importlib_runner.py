import sys
import os
import json
import importlib.util

def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

if __name__ == '__main__':
    out_dir = os.environ["OUT_DIR"]
    file_path = sys.argv[1]
    attribute_name = sys.argv[2]
    serialized_kwargs = sys.argv[3]

    assert os.path.isfile(file_path), "Specified file path does not exist: %s" % file_path
    module = import_from_path('dynamic.module.name', file_path)

    assert hasattr(module, attribute_name), "File has not attribute: %s" % attribute_name
    func = getattr(module, attribute_name)

    try:
        kwargs = json.loads(serialized_kwargs)
    except Exception as err:
        raise RuntimeError("Failed to decode kwargs as json: %s" % repr(serialized_kwargs)) from err

    result = func(**kwargs)

    out_path = os.path.join(out_dir, "out.json")
    with open(out_path, 'w') as f:
        # Little hacky to get most kinds of serialization working
        result = {"result": result}
        json.dump(result, f)