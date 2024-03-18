import sys
import socket
import cmd


class Shell(cmd.Cmd):
    def __init__(self, socket):
        super().__init__()
        self.s = socket

    def do_print(self, arg):
        t = 'print ' + arg
        self.s.sendall(t.encode())

    def do_info(self, arg):
        t = 'info ' + arg
        self.s.sendall(t.encode())

    def complete_info(self, text, line, begidx, endidx):
        DICT = ['host', 'port']
        return [c for c in DICT if c.startswith(text)]


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1617 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    Shell(s).cmdloop()
    print(s.recv(1024).rstrip().decode())
