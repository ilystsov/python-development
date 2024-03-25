import sys
import socket
import threading
import readline

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

def getmsg(sock):
    while res := sock.recv(1024).rstrip():
        print(f"{res}\n{readline.get_line_buffer()}", end='', flush=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    getter = threading.Thread(target=getmsg, args=(s,))
    s.connect((host, port))
    while msg := sys.stdin.buffer.readline():
        s.sendall(msg)
        print(s.recv(1024).rstrip().decode())
