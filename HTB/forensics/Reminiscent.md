
# Reminiscent 
https://app.hackthebox.com/challenges/reminiscent

Description: <br>
Suspicious traffic was detected from a recruiter&#039;s virtual PC. A memory dump of the offending VM was captured before it was removed from the network for imaging and analysis. Our recruiter mentioned he received an email from someone regarding their resume. A copy of the email was recovered and is provided for reference. Find and decode the source of the malware to find the flag.


## walkthrough

the file flounder-pc-memdump.elf is an windows memory dump. Analyse the dump with volatility3 

```bash
# list commands with whom processes got started
vol.py -f flounder-pc-memdump.elf windows.cmdline
```

This will output two powershell processes, that have base64 encoded scripts in their arguments. The flag is in the second powershell processes base64.