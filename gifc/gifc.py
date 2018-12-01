#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Interact with GitHub Gists using HTTP API

# python3 -m gifc -h
# ./gifc -h


import os
import subprocess
import tempfile
import yaml

import gifc.arrowshiv as arrowshiv
arrow = arrowshiv.importArrow()


##############################################################################
##############################################################################
##############################################################################
# gifc
##############################################################################

DEBUG = False
ERROR_SUFFIX = "Please try using the Web GUI."
TERM = os.environ.get('TERM', '')

ENABLE_COLOR = False
if '256color' in TERM.split('-'):
    ENABLE_COLOR = True

##############################################################################
#  Config / Environment
##############################################################################

try:
    EDITOR = os.environ.get('EDITOR', None)  # Default editor
    FALLBACK_EDITOR = 'nano'  # ;_; wish it was vim <3
    GH_USER = os.environ.get('GH_USER', None)
    GH_TOKEN = os.environ.get('GH_TOKEN', None)
    GH_BASE_URL = "https://api.github.com"
    HOME_DIR = os.path.expanduser("~")
    BINARY_DIR = os.path.dirname(os.path.realpath(__file__))
    WORKING_DIR = os.getcwd(),
except Exception as error:
    emsg = "FATAL Error during initialization: %s" % (error)
    print(emsg)
    exit(emsg)

# These are shared with __main__.py
args = []
argvars = {}
session = {}

##############################################################################
# Helpers - Output
##############################################################################


def term_width():
    ''' Determine Terminal width for output purposes '''
    width = 80
    try:
        width = os.get_terminal_size()[0]
    except Exception as e:
        msg = "FATAL Error with console/terminal: %s" % (e)
        printTerminal(msg)

    msg = f"Terminal is {width} wide."  # noqa fstring
    printDebug(msg)

    return width


class TMods:
    ''' Terminal Output Modifiers '''

    def __init__(self):
        self.modifiers = {
            '': '',
            'red': '\x1b[1;31;40m',
            'green': '\x1b[1;32;40m',
            'yellow': '\x1b[1;33;40m',
            'white': '\x1b[1;37;40m',
            'bold': '\033[1m',
            'end': '\x1b[0m'
        }

    def wrap(self, text, mod, end='end'):
        ''' Wrap Text with Modifier and Ending '''
        if ENABLE_COLOR:
            modCode = self.modifiers.get(mod)
            endCode = self.modifiers.get(end)
        else:
            results = f"{text}"
        results = f"{modCode}{text}{endCode}"

        # TODO Use this new wrap() method in printGist()
        return results

    def print(self, **kwargs):
        ''' Print Text using wrap() Method '''
        results = self.wrap(**kwargs)
        printTerminal(results)
        return results


def printGist(gist_list):
    ''' Print Each Element from Gist List '''

    fieldCurn = ':\t\t'
    results = []
    # Generate horizontal Gist separator
    sep = '<>'.center(term_width(), '-')
    top = '<List of Gists>'.center(term_width(), '-')

    mods = TMods()
    # Define Label for each Field, and value/styling
    humanizeMap = {
        'description': (
            'Description',
            ['bold', 'end'],
            ['green', 'end']
        ),
        'updated_at': (
            'Updated',
            ['bold', 'end'],
            ['red', 'end']
        ),
        'created_at': (
            'Created',
            ['bold', 'end'],
            ['red', 'end']
        ),
        'id': (
            'Gist ID:',
            ['bold', 'end'],
            ['', '']
        ),
        'fileList': (
            'File List',
            ['bold', 'end'],
            ['', '']
        ),
        'html_url': (
            'Web URL',
            ['bold', 'end'],
            ['green', 'end']
        ),
    }

    printTerminal(top)
    for gist in gist_list:
        # Create simplified File List
        fileList = list(gist.get("files").keys())
        gist.update({'fileList': fileList})
        for source, conf in humanizeMap.items():
            extraText = ''
            value = str(gist.get(source, ''))

            # Process fields ending in '_at'
            if 'at' == source.split('_')[-1]:
                try:
                    duration = arrow.get(value).humanize()
                    extraText = " (%s)" % (duration)
                    extraText = mods.wrap(extraText, 'white')
                except Exception as e:
                    printError(e, sysexit=False)

            # String/Modifier Defaults
            hString = ''
            fMod = ['', '']
            vMod = ['', '']

            try:
                hString = conf[0]
                fMod = conf[1]
                vMod = conf[2]
            except Exception as e:
                printError(e)

            value += extraText

            hFinal = mods.wrap(hString, *fMod)
            vFinal = mods.wrap(value, *vMod)

            line = f"{hFinal}{fieldCurn}{vFinal}"

            printTerminal(line)
            results.append(line)
        results.append(sep)
        printTerminal(sep)

    return results


def printError(msg, sysexit=True):
    ''' Print errors, and exit by default '''
    printmsg = "%s - %s" % (msg, ERROR_SUFFIX)

    if sysexit:
        exit(printmsg)
    else:
        print(printmsg)

    return printmsg


def printDebug(msg, prefix=''):
    ''' Print only with --debug '''
    if not DEBUG:
        return False

    if not prefix:
        prefix = 'DEBUG: '

    printmsg = '%s%s' % (
        prefix, msg
    )

    print(printmsg)
    return printmsg


def printTerminal(msg, prefix=''):
    ''' Print to Terminal/Output '''
    msg = "%s%s" % (prefix, msg)

    print(msg)
    return msg


def get_config_details(key):
    ''' Attempt to load configuration values '''

    # TODO Cache file as to only open and read a single time

    # Order-preserving tuple
    paths = (
        WORKING_DIR,
        HOME_DIR,
        f"{HOME_DIR}/.config",  # noqa
        BINARY_DIR
    )

    configFileName = '.gifc_config.yml'
    config = {}
    requiredConfigs = {
        'USER_ID': GH_USER,
        'TOKEN': GH_TOKEN
    }

    # Return default/specified Environment variables, if available
    defaultOverride = requiredConfigs.get(key)
    if defaultOverride:
        details = f"{len(defaultOverride)} for {key}"
        msg = "Found Environment Variable w. length of %s" % (details)
        printDebug(msg)
        result = defaultOverride
        return result

    # Retrieve value from file, weighted by path
    result = None
    for path in paths:
        fullpath = '%s/%s' % (path, configFileName)

        try:
            with open(fullpath, 'r') as f:
                msg = f"Found configuration file: {fullpath}"
                printDebug(msg)
                config = yaml.safe_load(f)
            if config:
                result = config.get(key, None)
                details = f"{len(result)} for {key}"
                msg = f"Found Config Variable w. length of {details}"
                printDebug(msg)
                break  # Stop looking for other configurations
        except FileNotFoundError:
            pass
        except Exception as e:
            printError(e)
    else:
        if not config:
            msg = "There were no valid configurations found. %s" % (
                configFileName
            )
            printError(msg)

        for required in requiredConfigs:
            result = config.get(required, None)
            if isinstance(result, None):
                msg = "You must provide %s key and non-Null value."
                printError(msg)

    # Return configuration value of key
    return result

##############################################################################
# Helpers - Functions
##############################################################################


def payload_generator(action, content=None, **kwargs):

    payload = {}
    url = ''
    s = {}

    gid = kwargs.get('gid', '')
    gistName = argvars.get('gh_file', '')
    uid = kwargs.get('user_id', '')
    files = kwargs.get('files', [])

    # Perform Action
    if action in ['get']:
        if uid:
            url = f"{GH_BASE_URL}/users/{uid}/gists"
        else:
            url = f"{GH_BASE_URL}/gists"

        s = getattr(session, 'get')
    elif action in ['create', 'update']:
        payload = {
            'description': argvars.get('description'),
            'public': argvars.get('public'),
            'files': {
                gistName: {
                    'content': content
                }
            }
        }
        # Update
        if gid:
            url = f"{GH_BASE_URL}/gists/{gid}"
            s = getattr(session, 'patch')
        # Create
        else:
            url = f"{GH_BASE_URL}/gists"
            s = getattr(session, 'post')
    elif action in ['delete', 'remove']:
        # Remove
        if files and gid:
            payload = {
                'files': dict(zip(files, [None] * len(files)))
            }
            url = f"{GH_BASE_URL}/gists/{gid}"
            s = getattr(session, 'patch')
        # Delete
        else:
            url = f"{GH_BASE_URL}/gists/{gid}"
            s = getattr(session, 'delete')

    # Validate Session
    if isinstance(s, dict):
        msg = '%s, %s, %s failed to create http session' % (
            action, content, kwargs
        )
        printError(msg)

    # Pop keys with null values in payload
    # This prevents issues with empty fields, such as description
    poplist = []
    for k, v in payload.items():
        if not v:
            poplist.append(k)
    printDebug(f"Poping keys: {poplist}")
    for p in poplist:
        del payload[p]

    printDebug(f"Generated Session: {s}")
    printDebug(f"Generated URL: {url}")
    printDebug(f"Generated Payload: {payload}")

    return s, url, payload

##############################################################################
##############################################################################
##############################################################################
# Main Functions/Methods for gifc CLI
##############################################################################


# Get/List Gists
##############################################################################
def gistRetrieve():
    ''' Retrieve n Gists '''

    # ref:  https://developer.github.com/v3/gists/#list-a-users-gists

    number_of_gists = args.number
    printTerminal('Retrieving %s Gists...' % (number_of_gists))

    s, url, payload = payload_generator('get', user_id=GH_USER)

    r = s(url, json=payload)
    printDebug(r.json())
    gist_list = []
    try:
        gist_list = r.json()[:number_of_gists]
    except Exception:
        pass

    printGist(gist_list)
    return gist_list


# Create or Update (Upsert) Gist
##############################################################################
def gistUpsert():
    ''' Create or Edit a Gist '''

    action = args.action
    created = False
    fileContents = None
    # gist_file = argvars.get('gh_file')
    gid = argvars.get('gist_id', None)
    message = argvars.get('message', '')
    file_ = argvars.get('file', None)
    # CLI String as source
    if message:
        fileContents = message
    # File as source

    elif file_:
        with open(file_, 'r') as f:
            fileContents = f.read()
    # Interactive/Live edit as source
    else:
        f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        f_name = f.name
        f.close()
        subprocess.run([EDITOR, f_name])
        with open(f_name) as f:
            fileContents = f.read()

    s, url, payload = payload_generator(args.action, fileContents, gid=gid)

    # Use Payload to Upsert Gist
    r = s(url, json=payload)

    # Create success = 201
    # Update success = 200
    c = r.status_code
    if 199 <= c <= 299:  # 2** Status Codes
        gid = r.json()['id']
        printTerminal("Gist %s successfully %s'd" % (gid, action))
        created = r.json().get('id', None)
    else:
        msg = f"Error {c} {action}'ing Gist"
        printError(msg)

    return created


# Delete Gists
##############################################################################
def gistDestroy():
    ''' Delete a Gist or Remove files from a Gist '''

    gid = args.gist_id
    fileList = argvars.get('remove', [])
    printTerminal(f'Deleting {gid} w. {len(fileList)} file(s): {fileList}!')

    s, url, payload = payload_generator(args.action, gid=gid, files=fileList)
    r = s(url, json=payload)

    # Delete success = 204
    # Remove success = 200
    # Idempotent success = 404
    c = r.status_code
    if (199 <= c <= 299) or c == 404:  # 2** + 404 Status Codes
        printTerminal(f'Gist {gid} deleted!')
    else:
        msg = f'Error response: {c}'
        printError(msg)

##############################################################################
