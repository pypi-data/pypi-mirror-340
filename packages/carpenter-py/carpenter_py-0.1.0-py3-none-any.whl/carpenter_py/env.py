from pathlib import Path

def find_project_root(markers=("root")) -> Path:
    current = Path(__file__).resolve()

    for parent in current.parents:
        if any((parent / marker).exists() for marker in markers):
            return parent

    return current.parents[2]

project_root = find_project_root()