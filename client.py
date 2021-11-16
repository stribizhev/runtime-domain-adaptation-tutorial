#!/usr/bin/env python3

import requests as req
import argparse as ag


def delete_all_updates(uuid):
    data = {
        'uid': uid,
    }
    res = req.post("TODO-url/delete", data=data)
    res.raise_for_status()

def translate(text, uid):
    data = {
        'input': text,
        'meta': {
            'uid': uid,
        }
    }
    res = req.post("TODO-url/translate", data=data)
    res.raise_for_status()
    translation = res.json()['output']
    return translation

def save(source, target, uuid):
    data = {
        'source': source,
        'target': target,
        'meta': {
            'uid': uid,
        }
    }
    res = req.post("TODO-url/translate", data=data)
    res.raise_for_status()

def translate_and_save(sources, targets, uuid):
    delete_all_updates(uuid)

    for source, target in zip(sources, targets):
        translation = translate(source, uuid)
        print(translation)
        save(source, target, uuid)



if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument('-s', '--source', type=ag.FileType('r', encoding='utf-8'), required=True)
    parser.add_argument('-t', '--target', type=ag.FileType('r', encoding='utf-8'), required=True)
    parser.add_argument('-u', '--uid', required=True)

    args = parser.parse_args()

    translate_and_save(args.source, args.target, args.uid)
