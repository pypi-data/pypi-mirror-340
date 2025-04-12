from argparse import ArgumentParser
import sys, json, re, os
from datetime import datetime
from urllib.parse import urlencode, quote
from urllib.request import urlopen, URLError, HTTPError

from etherdump.etherpad import Etherpad
from etherdump.commands.common import *
from time import sleep
from etherdump.commands.html5tidy import html5tidy
import html5lib
from xml.etree import ElementTree as ET
from fnmatch import fnmatch

# debugging
# import ElementTree as ET 

"""
pull(meta):
    Update meta data files for those that have changed.
    Check for changed pads by looking at revisions & comparing to existing


todo...
use/prefer public interfaces ? (export functions)


"""


def main (args):
    p = ArgumentParser("Check for pads that have changed since last sync (according to .meta.json)")

    p.add_argument("padid", nargs="*", default=[])
    p.add_argument("--glob", default=False, help="download pads matching a glob pattern")

    p.add_argument("--padinfo", default=".etherdump/settings.json", help="settings, default: .etherdump/settings.json")
    p.add_argument("--zerorevs", default=False, action="store_true", help="include pads with zero revisions, default: False (i.e. pads with no revisions are skipped)")
    p.add_argument("--pub", default="p", help="folder to store files for public pads, default: p")
    p.add_argument("--group", default="g", help="folder to store files for group pads, default: g")
    p.add_argument("--skip", default=None, type=int, help="skip this many items, default: None")
    p.add_argument("--meta", default=False, action="store_true", help="download meta to PADID.meta.json, default: False")
    p.add_argument("--text", default=False, action="store_true", help="download text to PADID.txt, default: False")
    p.add_argument("--html", default=False, action="store_true", help="download html to PADID.html, default: False")
    p.add_argument("--dhtml", default=False, action="store_true", help="download dhtml to PADID.diff.html, default: False")
    p.add_argument("--all", default=False, action="store_true", help="download all files (meta, text, html, dhtml), default: False")
    p.add_argument("--folder", default=False, action="store_true", help="dump files in a folder named PADID (meta, text, html, dhtml), default: False")
    p.add_argument("--output", default=False, action="store_true", help="output changed padids on stdout")
    p.add_argument("--force", default=False, action="store_true", help="reload, even if revisions count matches previous")
    p.add_argument("--no-raw-ext", default=False, action="store_true", help="save plain text as padname with no (additional) extension")
    p.add_argument("--fix-names", default=False, action="store_true", help="normalize padid's (no spaces, special control chars) for use in file names")

    p.add_argument("--css", default="/styles.css", help="add css url to output pages, default: /styles.css")
    p.add_argument("--script", default="/versions.js", help="add script url to output pages, default: /versions.js")

    p.add_argument("--nopublish", default="__NOPUBLISH__", help="no publish magic word, default: __NOPUBLISH__")

    args = p.parse_args(args)

    print ("etherdump version {}".format(VERSION), file=sys.stderr)

    with open(args.padinfo) as f:
        info = json.load(f)
    ep = Etherpad(info.get("apiurl"), info.get("apikey"))

    raw_ext = ".raw.txt"
    if args.no_raw_ext:
        raw_ext = ""

    if args.padid:
        padids = args.padid
    else:
        padids = ep.list()
        if args.glob:
            padids = [x for x in padids if fnmatch(x, args.glob)]

    padids.sort()
    numpads = len(padids)
    # maxmsglen = 0
    count = 0
    for i, padid in enumerate(padids):
        print (padid, file=sys.stderr)
        if args.skip != None and i<args.skip:
            continue
        progressbar(i, numpads, padid)
        try:
            result = ep.pad_pull(\
                    padid=padid, \
                    pub=args.pub, \
                    group=args.group, \
                    fix_names=args.fix_names, \
                    folder=args.folder, \
                    zerorevs=args.zerorevs, \
                    meta=args.all or args.meta, \
                    text=args.all or args.text, \
                    html=args.all or args.html, \
                    dhtml=args.all or args.dhtml, \
                    nopublish=args.nopublish, \
                    output=args.output, \
                    css=args.css, \
                    script=args.script, \
                    force=args.force, \
                    raw_ext = raw_ext
                )
            if result:
                count += 1
        except Exception as ex:
            print(f"EXCEPTION {padid}: {ex}")

    print("\n{0} pad(s) loaded".format(count), file=sys.stderr)
