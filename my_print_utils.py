def print_err(message):
    # ANSI escape code for red
    print(f"\033[91m[ERR] {message}\033[0m")

def print_inf(message):
    # ANSI escape code for green
    print(f"\033[92m[INF] {message}\033[0m")

def print_war(message):
    # ANSI escape code for green
    print(f"\033[93m[WAR] {message}\033[0m")
