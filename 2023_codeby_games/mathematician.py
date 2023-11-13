
#  nc 62.173.140.174 39001


import socket
import time
from sympy import symbols, Eq, solve



# Server configuration
host = '62.173.140.174'  # Localhost
port = 39001  # Port to bind to

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect((host, port))

# start the game
s.sendall(b'start\n')

time.sleep(1)


while True:
    response = s.recv(2048).decode().strip()
    lines_array = response.splitlines()
    print(response)

    for line in reversed(lines_array):
        if '=' in line:
            line = line.strip()

            print("line: " + line)

            brace_index = line.find('(')
            print("equation: " + line[brace_index+1])
            equal_index = line.find('=')

            close_brace_index = line.find(')')
            equation1 = line[close_brace_index+1:equal_index].strip()
            print("equation1: " + equation1)
            equation2 = line[equal_index+1:].strip()
            print("equation2: " + equation2)

            if 'x' in equation1:
                x = symbols('x')
                equation = Eq(eval(equation1), int(equation2))
                solution = solve(equation, x)
                print("solution: " + str(equation) +" = " + str(solution[0]))
            elif 'y' in equation1:
                y = symbols('y')
                equation = Eq(eval(equation1), int(equation2))
                solution = solve(equation, y)
                print("solution: " + str(equation) +" = " + str(solution[0]))

            send = str(solution[0]) + '\n'
            s.sendall(send.encode('utf-8'))
            time.sleep(1)
    time.sleep(1)

# Close the connection
s.close()