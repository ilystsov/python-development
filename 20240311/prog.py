import cmd

class Echoer(cmd.Cmd):
    """Dumb echo command REPL"""
    prompt = ':-> '
    words = "one", "two", "three", "four", "five"

    def do_echo(self, args):
        """echo any string"""
        print(args)

    def complete_echo(self, text, line, begidx, endidx):
        return [c for c in self.words if c.startswith(text)]

    def do_EOF(self, args):
        return True

    def emptyline(self):
        pass

if __name__ == "__main__":
    Echoer().cmdloop()