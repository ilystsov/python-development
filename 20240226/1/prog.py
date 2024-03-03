import cowsay


class Player:
    def __init__(self) -> None:
        self.x: int = 0
        self.y: int = 0


class Monster:
    def __init__(self, greetings_message: str) -> None:
        self.greetings_message: str = greetings_message


class MultiUserDungeon:
    def __init__(self, field_size: int) -> None:
        self.field_size = field_size
        self.player = Player()
        self.monsters = {}

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
        print(cowsay.cowsay(self.monsters[(x, y)].greetings_message))

    def add_monster(self, x: int, y: int, greetings_message: str) -> None:
        print(f"Added monster to ({x}, {y}) saying {greetings_message}")
        if (x, y) in self.monsters:
            print("Replaced the old monster")
        self.monsters[(x, y)] = Monster(greetings_message)

    def play(self) -> None:
        while True:
            try:
                command = input().split()
            except EOFError:
                break

            match command:
                case [('up' | 'down' | 'left' | 'right') as direction]:
                    self.move_player(direction)
                case ['addmon', *params]:
                    if len(params) == 3 and params[0].isdigit() and params[1].isdigit():
                        self.add_monster(int(params[0]), int(params[1]), params[2])
                    else:
                        print('Invalid arguments')
                case _:
                    print("Invalid command")


if __name__ == '__main__':
    MultiUserDungeon(10).play()
