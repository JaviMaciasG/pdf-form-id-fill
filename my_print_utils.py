def print_err(message, cont=False):
    prefix = "     " if cont else "[ERR]"
    # ANSI escape code for red
    print(f"\033[91m{prefix} {message}\033[0m")

def print_inf(message, cont=False):
    prefix = "     " if cont else "[INF]"
    # ANSI escape code for green
    print(f"\033[92m{prefix} {message}\033[0m")

def print_war(message, cont=False):
    prefix = "     " if cont else "[WAR]"
    # ANSI escape code for green
    print(f"\033[93m{prefix} {message}\033[0m")
