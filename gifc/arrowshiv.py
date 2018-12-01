#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @daryltucker

# This prevents a hard-dependency on arrow, until discussed.


# Soft dependency on arrow
def importArrow():
    ''' Import arrow, or create fallback Module/Class '''
    mod = {}
    try:
        import arrow
        mod = arrow
    except Exception as e:
        print("Unable to import arrow: %s" % (e))
        NO_ARROW = "some time ago"

        class arrow():
            ''' Fake Arrow Module '''

            def __init__(self, *args):
                return None

            def __getattr__(self, name):
                ''' Fallback Method '''
                def default(*args, **kwargs):
                    return self

                return default

            def humanize(self):
                return NO_ARROW

        mod = arrow()

    return mod

##############################################################################
