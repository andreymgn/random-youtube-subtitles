import argparse
import sys
import time
import random
from datetime import datetime

from urllib.error import HTTPError

from get_data import get_ids_api, get_ids_scrape, get_cc

def save_ids(ids):
    s = '\n'.join(ids)
    filename = '{}.lst'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    with open(filename, 'w') as f:
        f.write(s)
    return filename

def get_ids(f, n):
    ids = set()
    while len(ids) < n:
        time.sleep(1+random.uniform(0, 0.5))
        try:
            new_ids = f()
            ids |= new_ids
        except HTTPError:
            if len(ids) > 0:
                filename = save_ids(ids)
                print('HTTPError. Saving ids to file. Download subs from them later with main.py --download-subs --id-list {}'.format(filename))
            else:
                print('HTTPError. API quota exceeded or service unavailable')
            return []

    ids = list(ids)
    return ids

parser = argparse.ArgumentParser(description='Download captions from youtube videos')
group = parser.add_mutually_exclusive_group()
group.add_argument('--api', help='get video ids using youtube API', action='store_true')
group.add_argument('--scrape', help='get video ids by scraping youtube', action='store_true')
group.add_argument('--download-subs', help='download subtitles from file with video ids', action='store_true')
parser.add_argument('-n' help='number of videos to download captions from')
parser.add_argument('--api-key', help='youtube API key')
parser.add_argument('--id-list', help='file with video ids')
args = parser.parse_args()

if args.api:
    ids = get_ids(lambda: get_ids_api(args.api_key), args.n)
    get_cc(ids)
elif args.scrape:
    ids = get_ids(get_ids_scrape, args.n)
    get_cc(ids)
elif args.download_subs:
    s = ''
    with open(args.id_list) as f:
        s = f.read()
    get_cc(s.splitlines())

