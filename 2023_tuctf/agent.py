from pwn import *
import random

# Change logging level to help with debugging (error/warning/info/debug)
# ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING']
#context.log_level = 'debug'

def mapper():
    conn.sendlineafter(b':', 'HAHAHAHAHHAHAHAHAHAHAH')
    status = conn.recvuntil(b'Option: ', drop=True).decode('latin-1')
    print(status)
    print()
    print()
    conn.send(b'2\r\n')
    current = conn.recvuntil(b'Investigate:', drop=True).decode('latin-1')
    print("current: "+current)
    print()
    print()
    print()

    path = ['Attaya']
    with open('log.txt', 'a') as f:
        f.write("===================================================\n'\n")
        f.close()


    while True:
        city_options = []
        current = current.split('\n')

        for line in current:
            if line.startswith('- Current'):
                current_city = line.split(':')[1]
            elif line.startswith('- Next'):
                neighbours_splitted = line.split('|')
                for i in range(len(neighbours_splitted)):
                    if i % 2:  # if i is odd
                        city_options.append(neighbours_splitted[i].strip())
            elif line.startswith('- Description'):
                description = line.split(':')[1]
                
        next_city = random.choice(city_options)
        path.append(next_city)

        print("current_city: "+str(current_city))
        print("city_options: "+str(city_options))
        print("description: "+str(description))
        print("path: "+str(path))
        print()
        with open('log.txt', 'a') as f:
            f.write("current_city: "+str(current_city)+'\n')
            f.write("city_options: "+str(city_options)+'\n')
            f.write("description: "+str(description)+'\n')
            f.write("path: "+str(path)+'\n\n')
            f.close()

        conn.send(next_city + '\n')
        current = conn.recvuntil(b'Investigate:', drop=True).decode('latin-1')


def get_path():
    success = False
    path_costs = {}

    while not success:
        neighbours = {
            'Attaya': {
                'Belandris': 10, 
                'Delato': 5, 
                'Charity': 3
            },
            'Charity': {
                'Belandris': 8,
                'Emell': 2,
                'Flais': 8, 
                'Attaya': 3, 
                'Haphsa': 3,
                'Delato': 1, 
            },
            'Haphsa': {
                'Iyona': 8,
                'Kepliker': 7,
                'Melyphora': 8,
                'Queria': 10,
                'Delato': 1,
            },
            'Melyphora': {
                'Partamo': 4,
                'Shariot': 11,
                'Queria': 1,
            },
            'Queria': {
                'Partamo': 1,
                'Rhenora': 6,
                'Shariot': 10,
            },
            'Partamo': {
                'Osiros': 1,
                'Rhenora': 5,
                'Shariot': 9,
            },
            'Flais': {
                'Gevani': 3,
                'Iyona': 3,
                'Haphsa': 1, 
            },
            'Delato': {
                'Flais': 5,
                'Iyona': 5,
                'Belandris': 3,
            },
            'Belandris': {
                'Jolat': 15,
                'Gevani': 8,
                'Emell': 1,
            },
            'Jolat': {
                'Osiros': 7, 
                'Leter': 4, 
                'Kepliker': 5, 
            },
            'Gevani': {
                'Jolat': 8,
                'Iyona': 1,
                'Haphsa': 6,
            },
            'Emell': {
                'Gevani': 5, 
                'Iyona': 3, 
                'Flais': 5, 
            },
            'Iyona': {
                'Jolat': 15, 
                'Leter': 4,
                'Kepliker': 3, 
            },
            'Kepliker': {
                'Leter': 5,
                'Osiros': 2,
                'Partamo': 6,
                'Queria': 7,
                'Delato': 2,
                'Melyphora': 5,
            },
            'Leter': {
                'Osiros': 3, 
                'Rhenora': 10,
            },
            'Osiros': {
                'Shariot': 8,
                'Rhenora': 6, 
            },
            'Rhenora': {
                'Notasto': 2,
                'Shariot': 1, 
            },
            'Notasto': {
                'Shariot': 7
            },
        }

        current_city = 'Attaya'
        path = ['Attaya']
        path_cost = 0
        i = 0

        while neighbours[current_city] != {}:
            new_city = random.choice(list(neighbours[current_city].keys()))
            path_cost += neighbours[current_city][new_city]
            #print("i: "+str(i))
            #print("current_city: "+current_city+" "+str(neighbours[current_city]))
            #print("path_cost: "+str(path_cost))
            #print("path: "+str(path))
            #print()

            current_city = new_city
            path.append(new_city)
            i += 1

            if current_city == 'Shariot':
                path_costs[path_cost] = path
                break

        # find path with lowest cost:
        try:
            lowest_cost = min(path_costs.keys())
        except ValueError:
            continue

        print("cost: "+str(lowest_cost)+", path: "+str(path_costs[lowest_cost]))



# MAPPING

#while True:
#    try:
#        print("===================================================")
#        print("trying to connect...")
#        conn = remote('chal.tuctf.com', 30012)
#        print("executing mapper()")
#        print()
#        print()
#        mapper()
#        print("closing connection...")
#        conn.close()
#        sleep(1)
#    except EOFError:
#        continue


# GET PATH
get_path()
