import io

import cowsay


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
    def __init__(self, name: str, greetings_message: str) -> None:
        self.greetings_message: str = greetings_message
        self.name = name

class MultiUserDungeon:
    def __init__(self, field_size: int) -> None:
        self.field_size = field_size
        self.player = Player()
        self.monsters = {}
        self.custom_monsters = {'jgsbat': jgsbat}

    def move_player(self, direction: str) -> None:
        delta_x, delta_y = 0, 0
        if direction == 'up':
            delta_y = -1
        elif direction == 'down':
            delta_y = 1
        elif direction == 'left':
            delta_x = -1
        elif direction == 'right':
            delta_x = 1

        self.player.x = (self.player.x + delta_x) % self.field_size
        self.player.y = (self.player.y + delta_y) % self.field_size

        print(f'Moved to ({self.player.x}, {self.player.y})')

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

    def add_monster(self, name: str, x: int, y: int, greetings_message: str) -> None:
        if name not in cowsay.list_cows() and name not in self.custom_monsters:
            print("Cannot add unknown monster")
            return

        print(f"Added monster {name} to ({x}, {y}) saying {greetings_message}")
        if (x, y) in self.monsters:
            print("Replaced the old monster")
        self.monsters[(x, y)] = Monster(name, greetings_message)

    def play(self) -> None:
        print("<<< Welcome to Python-MUD 0.1 >>>")
        while True:
            try:
                command = input().split()
            except EOFError:
                break

            match command:
                case [('up' | 'down' | 'left' | 'right') as direction]:
                    self.move_player(direction)
                case ['addmon', *params]:
                    if len(params) == 4 and params[1].isdigit() and params[2].isdigit():
                        self.add_monster(params[0], int(params[1]), int(params[2]), params[3])
                    else:
                        print('Invalid arguments')
                case _:
                    print("Invalid command")


if __name__ == '__main__':
    MultiUserDungeon(10).play()
