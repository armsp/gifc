## TODO
0. Ability to just append to a gist.
1. Add support to update a file in a gist with the contents of a local file
2. Use urllib instead of requests so that only standard libraries are used
3. Improve the arguements.
4. Make it more intuitive to use.
5. Add Demo gif
6. Make it callable from cli itself i.e remove any `config.yml` files
 - Environment Variables
  >$ export DUMMY="dum dum" <br> $ python3 <br> >>> import os <br> >>> "DUMMY" in os.environ <br> True <br> >>> os.environ['DUMMY'] <br> 'dum dum'<br>
  Shell, shell and its processes, local, systemwide [environment var setup](https://askubuntu.com/questions/58814/how-do-i-add-environment-variables)
7. Seeing the contents of the file you want to append to or edit..  
POC   
```python
import os
import requests
import tempfile
import subprocess

f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
n = f.name
config = {'USER_ID': 'xxx', 'TOKEN': 'yyy'}
r = requests.get('https://api.github.com/gists/3a081894e8ea725dceb0f13db5a1f0c9')
content = r.json()['files']['tips.md']['content']
#print(content)
f.write(content)
f.close()
subprocess.run(['nano', n])
with open(n) as f:
    print (f.read())
f.close()
os.remove(n)
```
## It is NOT meant to replace the GUI neither does it attempt to.

## Features we will never have
1. Add support for creating multiple file gists
2. Add support to update multiples in a gist
