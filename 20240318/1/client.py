import io
from typing import Any

import cowsay
import shlex
import cmd
import sys
import socket

jgsbat = cowsay.read_dot_cow(
    io.StringIO(
        """
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))EOC
"""
    )
)


class MultiUserDungeonShell(cmd.Cmd):
    intro = "<<< Welcome to Python-MUD 0.1 >>>"
    prompt = "Python-MUD >> "

    def __init__(self, socket) -> None:
        super().__init__()
        self.socket = socket
        self.custom_monsters: dict[str, Any] = {"jgsbat": jgsbat}


    def move(self, direction: str) -> None:
        delta_x, delta_y = 0, 0
        if direction == "up":
            delta_y = -1
        elif direction == "down":
            delta_y = 1
        elif direction == "left":
            delta_x = -1
        elif direction == "right":
            delta_x = 1
        self.socket.sendall(f"move {delta_x} {delta_y}".encode())
        server_response = shlex.split(self.socket.recv(1024).decode())
        new_x, new_y, encounter_flag, monster_name, monster_message = server_response
        print(f"Moved to ({new_x}, {new_y})")
        if encounter_flag == "True":
            if monster_name in self.custom_monsters:
                print(cowsay.cowsay(monster_message, cowfile=self.custom_monsters[monster_name]))
            else:
                print(cowsay.cowsay(monster_message, cow=monster_name))

    def do_up(self, arg: str) -> None:
        self.move("up")

    def do_down(self, arg: str) -> None:
        self.move("down")

    def do_left(self, arg: str) -> None:
        self.move("left")

    def do_right(self, arg: str) -> None:
        self.move("right")

    def parse_addmon(self, params: list) -> tuple:
        expected_params_length = 8
        if len(params) != expected_params_length:
            raise ValueError
        name = params[0]
        param_pos = 1
        hitpoints, x, y, greetings_message = [None] * 4
        while param_pos < expected_params_length:
            if params[param_pos] == "hello":
                if greetings_message is not None:
                    raise ValueError
                greetings_message = params[param_pos + 1]
                param_pos += 2
            elif params[param_pos] == "hp":
                if (hitpoints is not None) or (not params[param_pos + 1].isdigit()):
                    raise ValueError
                hitpoints = int(params[param_pos + 1])
                if hitpoints <= 0:
                    raise ValueError
                param_pos += 2
            elif params[param_pos] == "coords":
                if (
                    (x is not None)
                    or (y is not None)
                    or (not params[param_pos + 1].isdigit())
                    or (not params[param_pos + 2].isdigit())
                ):
                    raise ValueError
                x, y = int(params[param_pos + 1]), int(params[param_pos + 2])
                param_pos += 3
            else:
                raise ValueError
        return name, hitpoints, x, y, greetings_message

    def add_monster(
        self, name: str, hitpoints: int, x: int, y: int, greetings_message: str
    ) -> None:
        if name not in cowsay.list_cows() and name not in self.custom_monsters:
            print("Cannot add unknown monster")
            return
        self.socket.sendall(f"addmon {name} {x} {y} {greetings_message}".encode())
        print(f"Added monster {name} to ({x}, {y}) saying {greetings_message}")
        server_response = shlex.split(self.socket.recv(1024).decode())
        replaced_flag = server_response
        if replaced_flag == "True":
            print("Replaced the old monster")

    def do_addmon(self, arg: str) -> None:
        params = shlex.split(arg)
        name, hitpoints, x, y, greetings_message = self.parse_addmon(params)
        self.add_monster(name, hitpoints, x, y, greetings_message)

    def do_EOF(self, arg: str) -> bool:
        return True


if __name__ == "__main__":
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        MultiUserDungeonShell(s).cmdloop()

