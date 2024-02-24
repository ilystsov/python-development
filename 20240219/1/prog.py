import sys 
import glob
from pathlib import Path
import zlib

def show_branches_names(path):
    if path[-1] == '/':
        path = path[:-1]
    for path in glob.iglob(path + '/.git/refs/heads/*'):
        name = Path(path).name
        print(name)

def show_last_commit(path, branch_name):
    if path[-1] == '/':
        path = path[:-1]

    path_to_branch = path + f'/.git/refs/heads/{branch_name}'
    with open(path_to_branch, 'r') as branch_file:
        commit_id = branch_file.read().rstrip()

    path_to_commit = path + f'/.git/objects/{commit_id[0:2]}/' + commit_id[2:]
    with open(path_to_commit, 'rb') as commit_file:
        bulk = zlib.decompress(commit_file.read())
    _, _, content = bulk.partition(b'\x00')
    content_parts = content.decode().split('\n')
    print(content_parts[0])
    print(content_parts[1])
    print(' '.join(content_parts[2].split(' ')[:-2]))
    print(' '.join(content_parts[3].split(' ')[:-2]))
    print()
    print(content_parts[5])
    
def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
        show_branches_names(path)
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        branch_name = sys.argv[2]
        show_last_commit(path, branch_name)
main()