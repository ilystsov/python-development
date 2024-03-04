import shlex


while True:
    s = input()
    print(shlex.join(shlex.split(s)))