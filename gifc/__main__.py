#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Interact with GitHub Gists using HTTP API
# python3 -m gifc -h
# ./gifc -h

__license__ = "GPL"

import argparse
import requests

# Import gifc Modules
from . import gifc
from .gifc import printDebug, get_config_details

##############################################################################
##############################################################################
##############################################################################
#  gifc
##############################################################################

# SEE gifc.py

##############################################################################
#  argparse
##############################################################################

parser = argparse.ArgumentParser(
    description='Interact with GitHub Gists via command-line interface.'
)
sp = parser.add_subparsers(dest='action')
sp.required = True

# 'Global' Arguments available to all Actions/parsers
parser_global = argparse.ArgumentParser(add_help=False)
parser_global.add_argument(
    '--debug', required=False,
    action='store_true',
    default=False,
    help='Enable debug output.'
)
parser_global.add_argument(
    '-e', '--editor', required=False,
    action='store',
    help='Use an editor other than bash default $EDITOR.'
)
parser_global.add_argument(
    '--public', required=False,
    action='store_true',
    default=False,
    help='Make a public Gist. Omit for default, private Gist.')

# Retrieve/GET Gist(s) ------
# Copy/Extend Global Arguments via `parents=[]`
p1 = sp.add_parser(
    'get',
    parents=[parser_global],
    help="Retrieve Gists from GitHub."
)
p1.add_argument(
    'number',
    default=5,
    type=int,
    help='Get <number> Gists and their descriptions.'
)

# Create Gist ------
p2 = sp.add_parser(
    'create',
    parents=[parser_global],
    help="Create a new Gist on GitHub."
)
p2.add_argument(
    '-fn', '--gh_file', required=True,
    help='Remote filename of Gist.'
)
p2.add_argument(
    '-d', '--description', required=False,
    default='',
    help='Description of Gist.'
)

# Only ONE of the following at a time:
p2_mutex = p2.add_mutually_exclusive_group()
p2_mutex.add_argument(
    '-m', '--message',
    help='Gist contents from CLI as string.'
)
p2_mutex.add_argument(
    '-f', '--file',
    help='Gist contents from a local file'
)
# TODO DRY Up Create/Update and Delete/Remove parsers to share common code
help_text_interactive = 'Use editor to define Gist after save/close. %s' % (
    "See --editor. Default $EDITOR."
)
p2_mutex.add_argument(
    '-i', '--interactive',
    action='store_true',
    default=False,
    help=help_text_interactive
)

# Update Gist ------
p3 = sp.add_parser(
    'update',
    parents=[parser_global],
    help='Update an existing Gist.'
)
p3.add_argument(
    'gist_id',
    help='Gist ID (hash) of the Gist you want to update.'
)
p3.add_argument(
    '-fn', '--gh_file', required=True,
    help='Remote filename of Gist.'
)
p3.add_argument(
    '-d', '--description', required=False,
    default='',
    help='Description of Gist.'
)

# Only ONE of the following at a time:
p3_mutex = p3.add_mutually_exclusive_group()
p3_mutex.add_argument(
    '-m', '--message',
    help='Gist contents from CLI as string.'
)
p3_mutex.add_argument(
    '-f', '--file',
    help='Gist contents from a local file.'
)
p3_mutex.add_argument(
    '-i', '--interactive',
    action='store_true',
    default=False,
    help=help_text_interactive
)

# Delete Gist
p4 = sp.add_parser(
    'delete',
    parents=[parser_global],
    help="Delete a Gist. DANGER! No recovery!"
)
p4.add_argument(
    'gist_id',
    help='Gist ID (hash) of the Gist you want to delete.'
)

# Delete files
p5 = sp.add_parser(
    'remove',
    parents=[parser_global],
    help='Remove individual files from a specific Gist.'
)
p5.add_argument(
    'gist_id',
    help='Gist ID (hash) of the Gist from which files will be removed.'
)
p5.add_argument(
    '-r', '--remove', required=True,
    nargs='+',
    help='File(s) you want to remove from a gist.'
)


##############################################################################
#  Runtime
##############################################################################


def main():

    # Process Arguments
    args = parser.parse_args()
    argvars = vars(args)

    # TODO Better way?
    # Set gifc args and argvars vars
    gifc.args = args
    gifc.argvars = argvars

    DEBUG = argvars.get('debug', False)
    # Update Module w. DEBUG flag
    gifc.DEBUG = DEBUG
    printDebug("DEBUG Enabled.")

    # Use Default $EDITOR, unless asked to use a specific editor
    # We trust the User knows valid binaries instead of restricting to list
    if argvars.get('editor', None):
        gifc.EDITOR = argvars.get('editor')
        printDebug(f"Switcing to {gifc.EDITOR} editor via CLI flag.")
    # We fallback if an editor is not defined
    if not gifc.EDITOR:
        gifc.EDITOR = gifc.FALLBACK_EDITOR
    printDebug(f"Selected {gifc.EDITOR} as editor.")

    # Create Session for headers and credentials
    userID = get_config_details('USER_ID')
    userToken = get_config_details('TOKEN')
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {userToken}"
    })
    gifc.session = session
    printDebug("Created http session w. authorization details.")

    uTS = userToken[:5]
    printDebug(
        f"Using credentials {userID}:{uTS}... against {gifc.GH_BASE_URL}."
    )

    actionMap = {
        'gistRetrieve': ['get'],
        'gistUpsert': ['create', 'update'],
        'gistDestroy': ['delete', 'remove']
    }

    commandFn = None
    for fnName, actionList in actionMap.items():
        if args.action in actionList:
            commandFn = getattr(gifc, fnName)
            break

    if commandFn:
        commandFn()
        exit()


if __name__ == "__main__":
    main()

##############################################################################
