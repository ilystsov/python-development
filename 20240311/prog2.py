import calendar
import cmd
import shlex


class Calendar(cmd.Cmd):
    Months = {m.name: m.value for m in calendar.Month}
    def do_prmonth(self, arg):
        year, month = shlex.split(arg)
        calendar.TextCalendar().prmonth(int(year), int(month))

    def complete_prmonth(self, text, line, bidx, eidx):
        if len(line.split()) >= 2:
            return [m for m in self.Months if m.startswith(text)]

    def do_pryear(self, arg):
        calendar.TextCalendar().pryear(int(arg))


if __name__ == "__main__":
    Calendar().cmdloop()