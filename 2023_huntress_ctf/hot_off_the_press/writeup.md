
# hot off the press

## Itroduction
Author: @JohnHammond
Oh wow, a malware analyst shared a sample that I read about in the news! https://www.huntress.com/blog/critical-vulnerabilities-ws_ftp-exploitation
But it looks like they put it in some weird kind of archive...? Anyway, the password should be infected as usual!

given is a file "hot_off_the_press"

## solve

file is UHarc archive 
extract with uharc.exe tool downloaded from: http://fileformats.archiveteam.org/wiki/UHARC

due to following lines in the powershell script you notice that the payload is base64 encoded and gzipped. 
```ps1
New-Object System.IO.StreamReader(
    New-Object System.IO.Compression.GzipStream((
        New-Object System.IO.MemoryStream(
            ,[System.Convert]::FromBase64String(((
```

Remove ''+'' with "search and replace" from the base64 string after "FromBase64String(((". The script uses formatted strings as obfuscation technique, " -f''L'',''E'' " signifies that the string is an formatted string, so replace every {0} with "L" and every {1} with "E. The python script decode.py will decode the base64string. then find another base64 string, which will contain after a lot of whitespace (ICAg) an url with the flag urlencoded as parameter.
