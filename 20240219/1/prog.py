import sys 
import glob
from pathlib import Path

def show_branches_names(path):
    if path[-1] == '/':
        path = path[:-1]
    for path in glob.iglob(path + '/.git/refs/heads/*'):
        name = Path(path).name
        print(name)

def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
        show_branches_names(path)

main()