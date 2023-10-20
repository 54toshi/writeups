
# Thumb Drive
People say you shouldn't plug in USB drives! But I discovered this neat file on one that I found in the parking lot...

## Instructions

1. use exiftool to extract an url out of the ADATA_128GB.lnk file
2. convert the base32 code found on the google drive to an executable DLL
3. now there are 3 ways:
    - run DLL with: rundll32.exe thumb_drive.dll, anything
    - extract strings with floss: https://github.com/mandiant/flare-floss
    - you could just reverse it

blog post on rundll32.exe: https://www.cybereason.com/blog/rundll32-the-infamous-proxy-for-executing-malicious-code