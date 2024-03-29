import io
import cowsay
import shlex


jgsbat = cowsay.read_dot_cow(io.StringIO('''
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
'''))


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
        self.field_size = field_size
        self.player = Player()
        self.monsters = {}
        self.custom_monsters = {'jgsbat': jgsbat}

    def move_player(self, direction: str) -> None:
        delta_x, delta_y = 0, 0
        if direction == "up":
            delta_y = -1
        elif direction == "down":
            delta_y = 1
        elif direction == "left":
            delta_x = -1
        elif direction == "right":
            delta_x = 1

        self.player.x = (self.player.x + delta_x) % self.field_size
        self.player.y = (self.player.y + delta_y) % self.field_size

        print(f"Moved to ({self.player.x}, {self.player.y})")

        if (self.player.x, self.player.y) in self.monsters:
            self.encounter(self.player.x, self.player.y)

    def encounter(self, x: int, y: int) -> None:
        monster = self.monsters[(x, y)]
        text = monster.greetings_message
        name = monster.name
        if name in self.custom_monsters:
            print(cowsay.cowsay(text, cowfile=self.custom_monsters[name]))
        else:
            print(cowsay.cowsay(text, cow=name))


    def add_monster(
        self, name: str, hitpoints: int, x: int, y: int, greetings_message: str
    ) -> None:
        if name not in cowsay.list_cows() and name not in self.custom_monsters:
            print("Cannot add unknown monster")
            return

        print(f"Added monster {name} to ({x}, {y}) saying {greetings_message}")
        if (x, y) in self.monsters:
            print("Replaced the old monster")
        self.monsters[(x, y)] = Monster(name, greetings_message, hitpoints)

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
                    (x is not None) or (y is not None)
                    or (not params[param_pos + 1].isdigit())
                    or (not params[param_pos + 2].isdigit())
                ):
                    raise ValueError
                x, y = int(params[param_pos + 1]), int(params[param_pos + 2])
                param_pos += 3
            else:
                raise ValueError
        return name, hitpoints, x, y, greetings_message

    def play(self) -> None:
        print("<<< Welcome to Python-MUD 0.1 >>>")
        while True:
            try:
                command = shlex.split(input())
            except EOFError:
                break

            match command:
                case [("up" | "down" | "left" | "right") as direction]:
                    self.move_player(direction)
                case ["addmon", *params]:
                    try:
                        name, hitpoints, x, y, greetings_message = self.parse_addmon(
                            params
                        )
                        self.add_monster(name, hitpoints, x, y, greetings_message)
                    except ValueError:
                        print("Invalid arguments")
                case _:
                    print("Invalid command")


if __name__ == "__main__":
    MultiUserDungeon(10).play()
