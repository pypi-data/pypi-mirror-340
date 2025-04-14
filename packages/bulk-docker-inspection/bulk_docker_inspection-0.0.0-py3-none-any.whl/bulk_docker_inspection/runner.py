import sys
import os
import json
import cloudpickle

if __name__ == '__main__':
    pickle_path = sys.argv[1]
    kwargs = sys.argv[2]

    assert os.path.isfile(pickle_path), "Specified pickle path does not exist: %s" % pickle_path
    with open(pickle_path, 'rb') as f:
        func = cloudpickle.load(f)

    try:
        kwargs = json.loads(kwargs)
    except Exception as err:
        raise RuntimeError("Failed to decode kwargs as json: %s" % repr(kwargs)) from err

    result = func(**kwargs)

    out_path = "/bdi_out/data.json"
    if not os.path.exists(out_path):
        data = {}
    else:
        with open(out_path, "r") as f:
            data = json.load(f)

    if pickle_path not in data:
        data[pickle_path] = {}
    data[kwargs] = result

    with open(out_path, 'w') as f:
        json.dump(data, f)
