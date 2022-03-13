import os
import subprocess

from typing import List


def parse_readme(readme_path: str):
    
    with open(readme_path, 'r') as f:
        readme = f.read()

    py_quot = '```python'
    sections = readme.split(py_quot)[1:]

    quot = '```'
    python = [s.split(quot)[0] for s in sections if quot in s]
    return python


def test_readme():
    paths = ['./README.md', '../README.md']
    for i, path in enumerate(paths):
        try:
            scripts = parse_readme(path)
            break
        except FileNotFoundError:
            if i == len(paths) - 1:
                raise FileNotFoundError
    assert len(scripts) != 0

    tmp_file = 'tmp_readme.py'
    for script in scripts:
        with open(tmp_file, 'w') as f:
            f.write(script)
        
        command: str = f'python3 {tmp_file}'
        args: list = command.split()

        result = subprocess.run(args, stdout=subprocess.PIPE)

        returncode: int = result.returncode
        success = returncode == 0
        if not success:
            stdout: str = result.stdout.decode()
            raise AssertionError(stdout)

    os.remove(tmp_file)
    return


if __name__ == '__main__':
    test_readme()

