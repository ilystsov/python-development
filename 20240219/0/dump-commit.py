import glob
import zlib
import sys
path = sys.argv[1]
for path in glob.iglob(path + '/??/*'):
    with open(path, 'rb') as f:
        content = f.read()
    decompressed = zlib.decompress(content)
    if decompressed.split()[0] == b'commit':
        print(decompressed.partition(b'\x00')[2].decode())
        