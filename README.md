# Gists From Command-line

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://www.python.org/) 
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/armsp/gifc/issues) 
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/armsp/disradicator/graphs/commit-activity) 
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) 



Welcome to the README of **gifc**.  

## NAME
gi-f-c : **Gi**_sts_ **f**_rom_ **c**_ommand-line_  

## ABOUT
This is a nifty little tool written in Python to work with GitHub Gists from command line. 

## Dependencies
* [requests](http://docs.python-requests.org/en/master/)
* [yaml](https://pyyaml.org/)

## **USAGE**
1. `chmod +x gifc`
2. Make a `gist_config.yml` file and enter your _secure token_ and _user_id_ as -
> TOKEN: xxxxx   
> USER_ID: yyyyy
3. Use it from cli as `./gifc <options> <flags>`
4. Or add it to PATH to call it as `gifc <options> <flags>`

**NOTE**  
Currently there is no way it can access your `gist_config.yml` file if you take the script inside `bin`. This feature will be added later on. So right now use it like **Step 2**

### **MANUAL**
`./gifc -h`

## **Example usage**
### **Get a list of gists**
`./gifc get 5`

### **Create a gist**
* Create interactively from an editor like **nano**, **vim** or **gedit**
    - ```./gifc create create.md -d "How to create a gist from cli" -i nano```
* Directly enter contents from cli
    - ```./gifc create create.md -d "How to create a gist from cli" -m '''If you want to create a gist from an existing file then you do the following-  `./gifc -c create.md -e "How to create a gist from cli" -i file.md`'''```
* Take the contents from a file
    - `./gifc create create.md -d "How to create a gist from cli" -f file.md`

### **Update a gist**
* Change description
    - `./gifc update ffd2f4a482684f56bf33c8726cc6ae63 -cd "New description"`  
    You can get the gist id from the `get` method from earlier

* Edit contents of a file interactively in an editor like **nano**, **vim** or **gedit**
    - `./gifc update ffd2f4a482684f56bf33c8726cc6ae63 -f file_to_update.md`
* Do both
    - `./gifc -u ffd2f4a482684f56bf33c8726cc6ae63 -f file_to_update.md -cd "New description"`

### **Delete file(s) from a gist**
`./gifc remove ffd2f4a482684f56bf33c8726cc6ae63 -r file1.md script.py readme.txt `  
You can get the gist id from the `get` method from earlier

### **Delete the whole gist**
`./gifc delete ffd2f4a482684f56bf33c8726cc6ae63`  
You can get the gist id from the `get` method from earlier

