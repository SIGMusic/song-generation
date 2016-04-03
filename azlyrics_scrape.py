import string
import urllib.request

def formatString(inString):
    formatOut = '';
    for c in inString:
        if c in string.ascii_lowercase or c in string.digits:
            formatOut += c
        elif c in string.ascii_uppercase:
            formatOut += c.lower()
    return formatOut;

def scrape(artist, song):
    reqArtist = formatString(artist)
    reqSong = formatString(song)
    reqURL = 'http://www.azlyrics.com/lyrics/' + reqArtist + '/' + reqSong + '.html'
    try:
        response = urllib.request.urlopen(reqURL)
    except HTTPError as e:
        if e.code == 404:
            print('Song not found')
        else:
            print('Error ' + e.code)
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
            lyrics = html[startIndex + len(startTag) : endIndex].replace('<br>', '')
            return lyrics

artist = input('Artist: ')
song = input('Song: ')
lyrics = scrape(artist, song)
print(lyrics)
