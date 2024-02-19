import glob
import sys
import zlib
path = sys.argv[1]
for path in glob.iglob(path + '/??/*'):
    with open(path, 'rb') as f:
        content = f.read()
    print(zlib.decompress(content))