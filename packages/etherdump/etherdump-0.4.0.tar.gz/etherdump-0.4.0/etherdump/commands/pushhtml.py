from etherdump.commands.sethtml import sethtml, pushhtml
import argparse
import os, sys
import json


def main(args):
    p = argparse.ArgumentParser("""Indiscriminantly PUSH the contents of dumped html files to an etherpad, clobbering any existing content!""")
    p.add_argument("input", nargs="+", help="Metadata files, e.g. *.meta.json")
    p.add_argument("--padinfo", default=".etherdump/settings.json", help="settings, default: .etherdump/settings.json")
    p.add_argument("--basepath", default=".")
    args = p.parse_args(args)

    with open(args.padinfo) as f:
        info = json.load(f)

    apiurl = info.get("localapiurl", info["apiurl"])
    apikey = info['apikey']
    for n in args.input:
        with open(n) as f:
            meta = json.load(f)
            for v in meta['versions']:
                if v['type'] == 'html':
                    path = v['path']
                    if args.basepath:
                        path = os.path.join(args.basepath, path)
                    break
            padid = meta['padid']
            with open(path) as f:
                htmlsrc = f.read()
            print ("Pushing {0} to {1}".format(path, padid), file=sys.stderr)
            pushhtml(apiurl, apikey, padid, htmlsrc)

