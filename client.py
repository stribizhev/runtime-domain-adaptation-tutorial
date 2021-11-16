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

    delete_all_updates(uuid)

def only_translate(url, sources, uuid):
    delete_all_updates(uuid)

    for source, target in sources:
        translation = translate(source, uuid)
        print(translation)


if __name__ == "__main__":
    parser = ag.ArgumentParser(description="Translates files by making requests to a runtime domain adaptation webservice. See https://github.com/marian-cef/marian-examples/tree/master/adaptive")
    parser.add_argument('url', metavar='TRANSLATION_SERVICE_URL',
                        help="URL to the runtime domain adaptation webservice")
    parser.add_argument('-s', '--source', type=ag.FileType('r', encoding='utf-8'), required=True,
                        help="The file to translate")
    parser.add_argument('-t', '--target', type=ag.FileType('r', encoding='utf-8'), required=False,
                        help="A file containing reference translations. Used to simulate a translator who's sending in post-edited translations.")
    parser.add_argument('-u', '--uid', required=True, help="Provide a random string to identify your sent in sentences.")

    args = parser.parse_args()

    if args.target is None:
        only_translate(args.url, args.source, args.uid)
    else:
        translate_and_save(args.url, args.source, args.target, args.uid)
