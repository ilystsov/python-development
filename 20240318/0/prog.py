import socket
import sys
import shlex

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1617 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while data := conn.recv(1024):
            data = shlex.split(data.decode())
            if data[0] == 'print':
                conn.sendall(shlex.join(data[1:]).encode())
            elif data[0] == 'info':
                if data[1] == 'host':
                    conn.sendall(str(addr[0]).encode())
                elif data[1] == 'port':
                    conn.sendall(str(addr[1]).encode())


