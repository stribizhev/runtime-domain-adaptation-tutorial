#!/usr/bin/env python3

import requests as req
import argparse as ag


def delete_all_updates(url, uuid):
    data = {
        'uid': uid,
    }
    res = req.post(f"{url}/delete", data=data)
    res.raise_for_status()

def translate(url, text, uid):
    data = {
        'input': text,
        'meta': {
            'uid': uid,
        }
    }
    res = req.post(f"{url}/save", data=data)
    res.raise_for_status()
    translation = res.json()['output']
    return translation

def save(url, source, target, uuid):
    data = {
        'source': source,
        'target': target,
        'meta': {
            'uid': uid,
        }
    }
    res = req.post(f"{url}/translate", data=data)
    res.raise_for_status()

def translate_and_save(url, sources, targets, uuid):
    delete_all_updates(uuid)

    for source, target in zip(sources, targets):
        translation = translate(source, uuid)
        print(translation)
        save(source, target, uuid)



if __name__ == "__main__":
    parser = ag.ArgumentParser(description="Translates files by making requests to a runtime domain adaptation webservice. See https://github.com/marian-cef/marian-examples/tree/master/adaptive")
    parser.add_argument('url', metavar='TRANSLATION_SERVICE_URL')
    parser.add_argument('-s', '--source', type=ag.FileType('r', encoding='utf-8'), required=True)
    parser.add_argument('-t', '--target', type=ag.FileType('r', encoding='utf-8'), required=True)
    parser.add_argument('-u', '--uid', required=True)

    args = parser.parse_args()

    translate_and_save(args.url, args.source, args.target, args.uid)
