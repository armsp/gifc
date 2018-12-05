# Gists From Command-line

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://www.python.org/) 
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/armsp/gifc/issues) 
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/armsp/disradicator/graphs/commit-activity) 
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) 



Welcome to the README of **gifc**.  

## ETYMOLOGY
gi-f-c : **Gi**_sts_ **f**_rom_ **c**_ommand-line_  

## Pronounciation
gifc: jif - sea

## ABOUT
This is a nifty little tool written in Python to work with GitHub Gists from command line. 

## Dependencies
* [requests](http://docs.python-requests.org/en/master/)

## **USAGE**
1. Get your [token](https://github.com/settings/tokens) with access to gists from Github.
    - Open the link and click on **Generate new token**
    - Type your password
    - Type a name for the token. Example: `gifc_<your name>`
    - Check the box for gists. (You can provide other permissions too)
2. Add your github _user_id_ and _token_ as **environment vaiables** to `.bashrc`. Append the following -
    > export GIT_TOKEN="xxxxx"   
    > export GIT_USER_ID="yyyyy"
3. To make sure that processes can access the new environment variables, run the following -
    ```bash
    source ~/.bashrc
    ```
4. Clone the repository (currently there is no pip package on PyPI, i intend to add it later)
5. Extract the contents
6. From inside the folder do the following based on your preferences -
    * If you want to keep getting the latest updates from GitHub (**RECOMMENDED**) by pulling them and you want it to reflect in your system as well, then it's best to install it in **development** mode as -
        ```bash
        pip3 install -e .
        ```
    * If you are satisfied with what you have right now, or you are unsure if you like it or you are just curious then install it the usual way -
        ```bash
        pip3 install .
        ```
7. Use it from cli as `gifc <options> <flags>`. Refer _Example usage_ below.
8. [ **OPTIONAL** ] If you want to _uninstall_ then do the following -
    ```bash
    sudo -H pip3 uninstall gifc
    ```



## **MANUAL**
`gifc -h`

## **Example usage**
### **Get a list of gists**
```gifc get 5```

### **Create a gist**
* Create interactively from an editor like **nano**, **vim** or **gedit**
    - ```gifc create create.md -d "How to create a gist from cli" -i nano```
* Directly enter contents from cli
    - ```gifc create create.md -d "How to create a gist from cli" -m '''If you want to create a gist from an existing file then you do the following-  `./gifc -c create.md -e "How to create a gist from cli" -i file.md`'''```
* Take the contents from a file
    - `gifc create create.md -d "How to create a gist from cli" -f file.md`

### **Update a gist**
* **Edit all (or some) files iteratively**
    - `gifc update ffd2f4a482684f56bf33c8726cc6ae63 -i vi`  
    You can get the _gist id_ from the `get` method from earlier

* **Change description**
    - `gifc update ffd2f4a482684f56bf33c8726cc6ae63 -cd "New description"`  
    You can get the _gist id_ from the `get` method from earlier

* **Edit contents of a file interactively in an editor like _nano_, _vim_ or _gedit_**
    - `gifc update ffd2f4a482684f56bf33c8726cc6ae63 -f file_to_update.md`
* **Do both**
    - `gifc update ffd2f4a482684f56bf33c8726cc6ae63 -f file_to_update.md -cd "New description"`

### **Delete file(s) from a gist**
`gifc remove ffd2f4a482684f56bf33c8726cc6ae63 -r file1.md script.py readme.txt `  
You can get the _gist id_ from the `get` method from earlier

### **Delete the whole gist**
`gifc delete ffd2f4a482684f56bf33c8726cc6ae63`  
You can get the _gist id_ from the `get` method from earlier

