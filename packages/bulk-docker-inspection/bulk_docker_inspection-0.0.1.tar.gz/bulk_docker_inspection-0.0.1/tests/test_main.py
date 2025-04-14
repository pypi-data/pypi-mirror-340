from pytest_unordered import unordered

import bulk_docker_inspection as bdi

# No failure if some result
# Arguments

def test_basic():
    inspection = bdi.BDI()
    py_version = inspection.add_func(
        bdi.samples.python_version,
        interpreter='python3'
    )
    uname = inspection.add_func(
        bdi.samples.uname_info,
        interpreter='python3',
    )


    results = inspection.inspect([
        "ros:iron",
        "ros:humble",
        "ros:galactic"
    ])

    print(results.data)
    assert list(results.func_results(py_version)) == unordered([
        (
            'ros:iron',
            '/usr/bin/python3: 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0]'
        ),
        (
            'ros:humble',
            '/usr/bin/python3: 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0]'
        ),
        (
            'ros:galactic',
            '/usr/bin/python3: 3.8.10 (default, Nov 22 2023, 10:22:35) \n[GCC 9.4.0]' # TODO: Wtf python why is there a '\n' here
        )
    ])
    assert list(results.func_results(uname)) == unordered([
        (
            'ros:iron',
            'Linux'
        ),
        (
            'ros:humble',
            'Linux'
        ),
        (
            'ros:galactic',
            'Linux'
        )
    ])