
# ekoparty ctf 03.11.2023

challenge files are on gopher web server. Use preferably lynx to connect to gopher server, but firefox works too.
- gopher service: go.ctf.site:10070

## UUEncrypted
files are found on gopher site at:
- http://go.ctf.site:10070/EKO/ENCRYPTED_1
- http://go.ctf.site:10070/EKO/ENCRYPTED_2

put them together and decrypt them with uudecoder like:
- https://toolslick.com/text/decoder/uudecode


## who 
given: "My friend Daniel has a secret between his fingers!" and go.ctf.site:10079

```bash
# first enumerate:
nmap -A -Pn -sV -vvv go.ctf.site -p 10079

# result:
# PORT      STATE SERVICE REASON  VERSION
# 10079/tcp open  finger  syn-ack Linux fingerd
# |_finger: No one logged on.\x0D
# Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

# use finger-user-enum perl script to get intel on user daniel
./finger-user-enum.pl -u daniel -p 10079 -t go.ctf.site
```

resources:
- https://book.hacktricks.xyz/network-services-pentesting/pentesting-finger
- https://pentestmonkey.net/tools/user-enumeration/finger-user-enum


## not slack
given: Communication is at the base of human progress, specially in tecnhology. We invite you to join the oldest and haxoristic network on the Internetz and read the message of the day!

go.ctf.site:16667

```bash
# first check what is running on port 16667
nmap -A -Pn -sV -vvv go.ctf.site -p 16667

# result:
# PORT      STATE SERVICE REASON  VERSION
# 16667/tcp open  irc     syn-ack
# | irc-info:
# |   users: 40
# |   servers: 2
# |   ops: 7
# |   chans: 32
# |   lusers: 33
# |   lservers: 1
# |   server: go.ctf.site
# |   version: UnrealIRCd-6.1.2.3. go.ctf.site
# |   source ident: nmap
# |   source host: CAF3F7A2.F600E4E1.D3E25E07.IP
# |_  error: Closing Link: ucnojxiro[212.95.31.145] (Quit: ucnojxiro)
# Service Info: Host: go.ctf.site
```
connect to IRC with IRC client like HexChat and type /motd to receive the message of the day and first IRC flag. 

## rulez
type: /rules  to get server rules and rulez flag

## admin
type: /admin  to get server admins and admin flag

## private
type: /list  to get list and topic of channels on server. The topic of the #private channel is the flag

also: /topic #private, /msg ChanServ info #private

## whois
tpye: /whois hds in #admin channel to get flag


# resources
writeups:
- https://xhacka.github.io/posts/writeup/2023/11/03/Github-Repo/

