import sys
import zlib
path = sys.argv[1]
with open(path, 'rb') as f:
    content = f.read()
print(zlib.decompress(content))