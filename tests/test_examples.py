import os
import subprocess


def test_examples():
    folders = ['./examples', '../examples']

    for folder in folders:        
        try:
            examples = os.listdir(folder)
        except FileNotFoundError:
            continue

        for ex in examples:
            command: str = f'python3 {folder}/{ex}'
            args: list = command.split()

            result = subprocess.run(args, stdout=subprocess.PIPE)
            success: bool = (result.returncode == 0)

            if not success:
                stdout: str = result.stdout.decode()
                raise AssertionError(stdout)
    return

