# Gists from Command-line

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://www.python.org/)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/armsp/gifc/issues)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/armsp/disradicator/graphs/commit-activity)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

------

> Welcome to the `gifc` README!

### `gifc` Overview
#### Etymology

> gi-f-c : **Gi**_sts_ **f**_rom_ **c**_ommand-line_

#### About
This is a nifty little tool written in Python to interact with GitHub Gists from command line.

#### Dependencies

* [requests](http://docs.python-requests.org/en/master/)
* [yaml](https://pyyaml.org/)
* [arrow](https://arrow.readthedocs.io/en/latest/) *Optional*

![Discuss arrow dependency](https://img.shields.io/badge/TODO-Discuss%20arrow%20dependency-lightgrey.svg)

### How to use `gifc`
#### Setup/Install
##### Configuration File:

1. Place `.gifc_config.yml` in your `$HOME`, `$HOME/.config`, current directory, or script directory.
    * Ensure this is a safe place to keep your credentials safeguarded
    * Note: Dot-files are sometimes hidden by file browsers

> Tokens are created via GitHub Website as Personal Access Tokens for API

```yaml
TOKEN: 123456
USER_ID: myGitHubName
```

##### Typical Installation using `setup.py`

> This is the best for non-Contributors, or those wishing only to use `gifc`.

![Publish to pip](https://img.shields.io/badge/TODO-Publish%20to%20pip-lightgrey.svg)

1. Clone the repository
1. Within the repository directory:
    * `python3 setup.py build`
    * `python3 setup.py install [--user --prefix=PREFIX]`
1. See: [Configuration File](Configuration-File)

After installing, you should see this output towards the end:

    Installing gifc script to /home/user/.local/bin

You must ensure that this directory is part of your `$PATH`:

    $ echo $PATH


##### Developer Installation using $PYTHONPATH

> This makes it easier to test your changes.

1. Clone the repository into your `$PYTHONPATH`
    1. `export $PYTHONPATH="${PYTHONPATH}:${HOME}/src/"`
    1. `git clone https://github.com/armsp/gifc ${HOME}/src/gifc`
1. See: [Configuration File](configuration-fileConfiguration-File)
1. `python -m gifc [options] <actions> <flags>`


------
#### Manual / Examples

    $ python -m gifc -h  # '$PYTHONPATH' install
    $ gifc -h  # pip or setup.py install

This will output supported 'actions', which will always be the first argument provided at runtime.

##### Retrieve/List N Gists

> `gifc get -h`

1. `gifc get 5`
    * Retrieve 5 Gists
1. `gifc get 5 --debug`
    * Retrieve 5 Gists in verbose mode

##### Create a Gist

When Creating or Updating Gists, the new Gist data can come from one of three sources:

1. A local file, using `-f "path/to/file"` flag
1. A string provided via CLI, using `-m "Message"`
1. Interactive editing using default or specified editor

**Create Examples**

> `gifc create -h`

1. `gifc create -fn "Remote_Filename.mkd" -f "/home/me/Local_Filename.mkd"`
    * `-d "A comment"` is an optional flag you can place after Action.  Defaults to empty string.
1. `gifc create -fn "Remote_Filename.mkd" -m "Short Gist"`
1. `gifc create -fn "Remote_Filename.mkd"`
    * Edit in $EDITOR, or `--editor` flag editor

##### Update a Gist

> `gifc update -h`

When Editing/Updating a Gist, we need to provide both the Remote Filename (`-fn`) and Gist ID (the hash).
All other syntax matches that of the previous `create` examples, we just add the identifier immediately after Action.

**Update Examples**

1. `gifc update GIST_ID_HASH -fn "Remote_Filename.mkd" -f "/home/me/Local_Filename.mkd"`

##### Delete/Remove a Gist or one or more files from a Gist

> `gifc delete -h`
> `gifc remove -h`

Gists can be a single file, or multiple files.  As such, you can Delete a Gist, or Remove files from a Gist.
This is why Updates require both `GIST_ID_HASH` as well as the remote filename (`-fn`).

**Delete/Remove Examples**

1. `gifc delete GIST_ID_HASH`
1. `gifc remove GIST_ID_HASH -r file1.md script.py readme.txt`

