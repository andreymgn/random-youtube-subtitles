import random
import json
import urllib.request
import string

from youtube_dl import YoutubeDL
from bs4 import BeautifulSoup

def get_ids_api(api_key):
    count = 50
    rnd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

    urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&videoCaption=closedCaption&q={}".format(api_key, count, rnd)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))
    
    ids = set()

    for data in results['items']:
        videoId = (data['id']['videoId'])
        ids.add(videoId)

    return ids

def get_ids_scrape():
    rnd = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

    query = urllib.parse.quote(rnd)
    url = 'https://www.youtube.com/results?search_query={}&sp=EgIoAQ%253D%253D'.format(query)
    response = urllib.request.urlopen(url)

    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    ids = set()
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if not vid['href'].startswith("https://googleads.g.doubleclick.net/"):
            id = vid['href'][9:]
            ids.add(id)
    return ids

def get_cc(ids, langs):
    opts = {
        'skip_download': True,
        'writesubtitles': True,
        'subtitleslangs': langs.split(','),
        'outtmpl': 'subs/%(id)s'
    }
    urls = ['https://youtube.com/watch?v={}'.format(id) for id in ids]
    ydl = YoutubeDL(opts)
    try:
        ydl.download(urls)
    except Exception as e:
        print('Exception when downloading:', e)

