import shlex
import sys
import socket


class Player:
    def __init__(self) -> None:
        self.x: int = 0
        self.y: int = 0


class Monster:
    def __init__(self, name: str, greetings_message: str, hitpoints: int) -> None:
        self.greetings_message: str = greetings_message
        self.name = name
        self.hitpoints = hitpoints


class MultiUserDungeon:
    def __init__(self, field_size: int) -> None:
        self.field_size: int = field_size
        self.player: Player = Player()
        self.monsters: dict[tuple[int, int], Monster] = {}
        self.weapons: dict[str, int] = {'sword': 10, 'spear': 15, 'axe': 20}
        self.custom_monsters: dict[str, Monster] = {"jgsbat": jgsbat}

    def encounter(self, x: int, y: int) -> tuple[str, str]:
        monster = self.monsters[(x, y)]
        text = monster.greetings_message
        name = monster.name
        return name, text

    def move_player(self, delta_x, delta_y):
        self.player.x = (self.player.x + delta_x) % self.field_size
        self.player.y = (self.player.y + delta_y) % self.field_size
        if (self.player.x, self.player.y) in self.monsters:
            name, text = self.encounter(self.player.x, self.player.y)
            return self.player.x, self.player.y, "True", name, text
        else:
            return self.player.x, self.player.y, "False", '', ''

    def add_monster(self, name, text, hp, x, y):
        self.monsters[(x, y)] = Monster(name, text, hp)
        if (x, y) in self.monsters:
            return "True"
        return "False"

    def serve(self, conn, addr):
        with conn:
            while data := conn.recv(1024):
                match shlex.split(data.decode()):
                    case ["move", x, y]:
                        conn.sendall(
                            shlex.join(self.move_player(int(x), int(y))).encode()
                        )
                    case ["addmon", name, hp, x, y, text]:
                        conn.sendall(self.add_monster(
                            name, text, int(hp), int(x), int(y)
                        ).encode())

if __name__ == "__main__":
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        multi_user_dungeon = MultiUserDungeon(10)
        multi_user_dungeon.serve(*s.accept())
