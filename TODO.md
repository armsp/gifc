## TODO
0. - [x] Callable as `gifc` from cli via `pip install gifc` as a script.(To be released in a week)
0. - [x] Ability to just append to a gist.
1. Add support to update a file in a gist with the contents of a local file
2. Get gist by id (`gifc get -id ffg564g4hfh..`)
3. Search gists based on keywords (display answer based on completeness of match) [`gifc search curry`]-
    * Search by title (`gifc search -t <title>`)
    * Search in description contents (`gifc search -d <description contents>`)
    * Search in gist contents (`gifc search -c <body content>`)
2. - [x] Use urllib instead of requests so that only standard libraries are used
    - **GET**ting the json data
    ```python
    import urllib.request
    url = 'https://jsonplaceholder.typicode.com/posts'
    r = urllib.request.urlopen(url).read()
    data = json.loads(r.decode('utf-8'))
    ```
    - **POST**ing the resource
    ```python
    import json
    import urllib.request
    import urllib.parse
    d = {"spam": 1, "eggs": 2, "bacon": 0}
    #data = urllib.parse.urlencode(d)
    data = json.dumps(d)
    data = data.encode()
    req = urllib.request.Request("http://localhost:5000/random", data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 12345)
    with urllib.request.urlopen(req) as f:
        print(f.read().decode('utf-8'))
    ```
    - **PATCH**ing the resource
    ```python
    req = urllib.request.Request("http://localhost:5000/random", data, method='PATCH')
    #req.get_method = lambda: 'PATCH'
    with urllib.request.urlopen(req) as f:
    print(f.read().decode('utf-8'))
    ```
    - **DELETE**ing the resource
    ```python
    req = urllib.request.Request("http://localhost:5000/random", data, method='DELETE')
    #req.get_method = lambda: 'DELETE'
    with urllib.request.urlopen(req) as f:
    print(f.read().decode('utf-8'))
    ```
 
3. - [x] Improve the arguements.
4. - [x] Make it more intuitive to use.
5. - [ ] Add Demo gif
6. Make it callable from cli itself i.e remove any `config.yml` files
    - Environment Variables
        >$ export DUMMY="dum dum" <br> $ python3 <br> >>> import os <br> >>> "DUMMY" in os.environ <br> True <br> >>> os.environ['DUMMY'] <br> 'dum dum'<br>

        * Shell, shell and its processes, local, systemwide [environment var setup](https://askubuntu.com/questions/58814/how-do-i-add-environment-variables)
7. - [x] Seeing the contents of the file you want to append to or edit.  
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
8. - [x] Creating gists from the editor  
POC  
```python
#!/usr/bin/env python3

import os
import tempfile
import subprocess
import argparse
import requests
import yaml

parser = argparse.ArgumentParser(description='Github gists from command line')

#Create gists
parser.add_argument('-c','--create', help='Full file name')
parser.add_argument('-d','--describe', help='Explain, elucidate or expound the gist')
parser.add_argument('-p','--public', help='Make a public gist', default=False)
#parser.add_argument('-m','--message', help='Gist contents as string')
#parser.add_argument('-i','--input', help='Input file name')

args = vars(parser.parse_args())

def get_config_details(key):
    try:
        with open('gist_config.yml', 'r') as f:
            config = yaml.safe_load(f)
    except:
        print('Configuration file not found')
        exit()
    else:
        if config.get(key):
            return config[key]
        else:
            if key == 'TOKEN':
                print('User token not found. Please add your token to gist_config.yaml')
                exit()
            elif key == 'USER_ID':
                print('User ID not found. Please add your github user_id to gist_config.yml')
                exit()
print('Configured...')
header = {"Authorization": f"Bearer {get_config_details('TOKEN')}"}

#./create.py -c "gist_file_name.md" -d "Some description for gist" -p True
f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
f_name = f.name
f.close()
subprocess.run(['nano', f_name])
with open(f_name) as f:
    contents = f.read()

payload = {'description': args['describe'], 'public': args['public'], 'files':{args['create']: {'content': contents}}}
r = requests.post(f"https://api.github.com/gists", headers=header, json=payload)
if r.status_code == 201:
    print(r.status_code)
    print(r.json()['id'])
    print('Gist successfully created')
else:
    print('Creating gist failed')
```
9. - [ ] Get method doesn't work for private gists. May have to use [OAuth](https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/) for that.
11. - [ ] Requests raises exceptions inherited from RequestException that you are not catching. So commands like `r = request.post(....)` can fail on bad internet connections or because other random issues. Catch them like -  
        ```python
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print e
        ```
        OR
        ```python
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print e
        ```
12. Handle FileNotFoundError in creating of gists via file parameter.
10. Instead of using `__file__` as in `foo_config = open(os.path.join(os.path.dirname(__file__),'foo.conf').read()` or ```cwd = os.path.dirname(os.path.abspath(__file__))```, use `pkg_resources` instead. [Help1](http://peak.telecommunity.com/DevCenter/PythonEggs#accessing-package-resources), [Help2](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#resourcemanager-api)
13. Displaying gists in cli
14. Update is still hardcoded with `nano`. Can we open it in system default editor?
15. If no file arguement and description is given in update then open the first file in that gist in interactive mode for editing ?
## It is NOT meant to replace the GUI neither does it attempt to.

## Features we will never have
1. Add support for creating multiple file gists
2. Add support to update multiple files in a gist
