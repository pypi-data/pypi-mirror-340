import json
from argparse import ArgumentParser
from etherdump.etherpad import Etherpad


def main(args):
    p = ArgumentParser("calls the getText API function for the given padid")
    p.add_argument("padid", help="the padid")
    p.add_argument("--padinfo", default=".etherdump/settings.json", help="settings, default: .etherdump/settings.json")
    p.add_argument("--showurl", default=False, action="store_true")
    p.add_argument("--format", default="text", help="output format, can be: text, json; default: text")
    p.add_argument("--rev", type=int, default=None, help="revision, default: latest")
    args = p.parse_args(args)

    with open(args.padinfo) as f:
        info = json.load(f)
    ep = Etherpad(info.get("apiurl"), info.get("apikey"))
    print(ep.pad_text(args.padid, args.rev, return_url=args.showurl))
