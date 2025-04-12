from __future__ import print_function
from argparse import ArgumentParser
import json
from urllib import urlencode
from urllib2 import urlopen, HTTPError, URLError


def main(args):
    p = ArgumentParser("call getRevisionsCount for the given padid")
    p.add_argument("padid", help="the padid")
    p.add_argument("--padinfo", default=".etherdump/settings.json", help="settings, default: .etherdump/settings.json")
    p.add_argument("--showurl", default=False, action="store_true")
    args = p.parse_args(args)

    with open(args.padinfo) as f:
        info = json.load(f)
    apiurl = info.get("apiurl")
    data = {}
    data['apikey'] = info['apikey']
    data['padID'] = args.padid.encode("utf-8")
    requesturl = apiurl+'getRevisionsCount?'+urlencode(data)
    if args.showurl:
        print (requesturl)
    else:
        results = json.load(urlopen(requesturl))['data']['revisions']
        print (results)
