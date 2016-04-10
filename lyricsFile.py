import urllib.request
import urllib.error
import json
import string
import re
import time
import lastfmAPI

proxy = {'http': 'http://54.174.29.183:8080'}
proxy_support = urllib.request.ProxyHandler(proxy)
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

def getSongs(tag, num):
    songsArray = []
    reqURL = 'http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag=' + tag.replace(' ', '+') + '&limit=' + str(num) + '&api_key=' + lastfmAPI.key() + '&format=json'
    try:
        response = urllib.request.urlopen(reqURL)
    except:
        print('Error')
        return songsArray
    else:
        data = json.loads(response.read().decode())
        for song in data['tracks']['track']:
            songsArray += [[song['artist']['name'], song['name']]]
        return songsArray

def formatString(inString):
    formatOut = '';
    for c in inString:
        if c in string.ascii_lowercase or c in string.digits:
            formatOut += c
        elif c in string.ascii_uppercase:
            formatOut += c.lower()
    return formatOut;

def scrapeLyrics(artist, song):
    if(artist[0:4] == 'The '):
        reqArtist = formatString(artist[4:])
    else:
        reqArtist = formatString(artist)
    reqSong = formatString(song)
    reqURL = 'http://www.azlyrics.com/lyrics/' + reqArtist + '/' + reqSong + '.html'
    try:
        response = urllib.request.urlopen(reqURL)
    except:
        print('Song not found')
        return ''
    else:
        html = response.read().decode()
        startTag = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        endTag = '</div>'
        startIndex = html.find(startTag)
        endIndex = html.find(endTag, startIndex)
        if startIndex == -1 or endIndex == -1:
            print('Parsing error')
            return ''
        else:
            lyrics = html[startIndex + len(startTag) : endIndex]
            lyrics = re.sub(r'<[^>]+>', '', lyrics)
            lyrics = re.sub(r'\[[^\]]+\]', '', lyrics)
            for char in ['&quot;', '\r', ',', '.', '!', '?', '(', ')', '~']:
                lyrics = lyrics.replace(char, '')
            return lyrics

urllib.request.urlopen('http://www.google.com')
tag = input('Tag: ')
num = input('Number of songs: ')
songs = getSongs(tag, num)
print(len(songs))
f = open('lyrics.txt', 'w')
for song in songs:
    print(song)
    songLyrics = scrapeLyrics(song[0], song[1])
    if(songLyrics != ''):
        f.write(songLyrics)
    time.sleep(1)
f.close()
