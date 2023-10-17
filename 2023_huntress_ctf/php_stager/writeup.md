
# php stager

## introduction
Author: @JohnHammond
Ugh, we found PHP set up as an autorun to stage some other weird shady stuff. Can you unravel the payload?
NOTE, this challenge is based off of a real malware sample. We have done our best to "defang" the code, but out of abudance of caution it is strongly encouraged you only analyze this inside of a virtual environment separate from any production devices.

## instructions

use decode.php from the repo to decode the encoded/encrypted code. i unobfuscated the code and printed the payload to stout. when decoded the php code, find the next base64 encoded string (line 1459) which is an perl script (callback.pl) with the uuencoded flag. 