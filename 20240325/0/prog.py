import http.server
import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
s.close()
port=sys.argv[1] if len(sys.argv) > 1 else "8000"
http.server.test(port=port, HandlerClass=http.server.SimpleHTTPRequestHandler)
