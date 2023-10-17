# tragedy redux

## instructions
We found this file as part of an attack chain that seemed to manipulate file contents to stage a payload. Can you make any sense of it?


## solve
extract (leave zip):
```
xz -d your_archive.tar.xz
tar -xvf your_archive.tar
```

use oletools to extract VBA (Visual Basic for Applications) macro code https://github.com/decalage2/oletools
```
pip install oletools
olevba openxml.zip -z infected -f word/vbaProject.bin > macro.vba
```

edit the code, so the encrypted string will be outputted to Debug console

