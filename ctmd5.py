#!/usr/bin/env python3

import argparse
import hashlib
import os
import random
import sys

__VERSION__ = '0.1.1'
CHARACTERS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_parser():
    parser = argparse.ArgumentParser(
        description='a cli tool used to change the MD5 of files',
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-f', '--file',
        metavar='FILE',
        type=str,
        help='the file you want to change md5',
    )
    group.add_argument(
        '-d', '--dir',
        metavar='DIR',
        type=str,
        help='change the md5 value for each of the files in a given directory',
    )
    parser.add_argument(
        '-s', '--show', action='store_true',
        help='show the md5 value'
    )
    parser.add_argument('-v', '--version',
                        action='version', version=__VERSION__)
    return parser


def get_md5(file):
    if os.path.exists(file):
        with open(file, 'rb') as f:
            md5 = hashlib.md5()
            while True:
                buffer = f.read(4096)
                if not buffer:
                    break
                md5.update(buffer)
            return md5.hexdigest()


def handle_single_file(file, show_md5=None):
    random_str = ''.join(random.choice(CHARACTERS))

    old = ''
    if show_md5:
        old = get_md5(file)

    with open(file, 'ab') as f:
        f.write(random_str.encode('utf-8'))

    new = get_md5(file)

    if show_md5:
        if old != new:
            print('[Success]The md5 value {0} has been changed from {1} to {2}'.format(file, old, new))
        else:
            print("[Failed]The md5 of file {0} before and after is the same,please check".format(file))
    else:
        if old != new:
            print("[Success]The md5 of file {0} has been changed.".format(file))
        else:
            print("[Failed]The md5 of file {0} before and after is the same,please check".format(file))


def change_the_md5(file_path=None, dir_name=None, show_md5=False):
    if file_path and os.path.exists(file_path):
        handle_single_file(file_path, show_md5)

    if dir_name and os.path.exists(dir_name):
        print("Found directory:", dir_name)
        for root, dirs, files in os.walk(dir_name):
            for f in files:
                file_path = os.path.join(root, f)
                handle_single_file(file_path, show_md5)


def cli():
    args = vars(get_parser().parse_args())
    file_path = args.get('file', None)
    dir_name = args.get('dir', None)
    show_md5 = args.get('show', None)

    change_the_md5(file_path=file_path, dir_name=dir_name, show_md5=show_md5)


if __name__ == '__main__':
    cli()
