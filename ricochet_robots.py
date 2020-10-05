def readInput(robots, target, barriers):
    n = input()
    for i in range(0, n):
        input_str = input()
        pos = input_str.split()
        robots.append(pos)
    input_str = input()
    target = input_str.split()
    n = input()
    for i in range(0, n):
        input_str = input()
        pos = input_str.split()
        barriers.append(pos)

