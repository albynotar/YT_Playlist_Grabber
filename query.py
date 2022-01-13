from urllib.parse import urlparse
import yt_dlp
import re

"""
Function that checks and cleans a query inserted as input.
The query must be a valid yt-playlist url to pass the validation.
"""


def check_query(query):
    if query == '':
        return False, 'Your Query is empty'
    # remove any special character from query
    url = re.sub(r'\s+', '', query)

    # adjusted query
    clear_url = ''

    # checks for a youtube domain
    if url.startswith('https://www.youtube.com/'):
        clear_url = str(url)
    elif url.startswith('//www.youtube.com/'):
        clear_url = str('https:') + str(url)
    elif url.startswith('www.youtube.com/'):
        clear_url = str('https://') + str(url)
    elif url.startswith('youtube.com/'):
        clear_url = str('https://www.') + str(url)

    # if the url does not contain a youtube url domain return False
    if clear_url == '':
        return False, 'Your Query is not a youtube link'

    # analyze the query using urlparse
    o = urlparse(clear_url)

    # if the link does not contain a playlist query return False
    if 'list=' not in o.query:
        return False, 'Your Query is not a youtube playlist url'

    # if the link does not contain a playlist id return False
    if o.query.endswith('list='):
        return False, 'Your Query does not contain a youtube playlist id'

    # options to extract info
    ydl_opts = {
        'forcejson': True,
        'ignoreerrors': True,
        'skip_download': True,
        'playlistrandom': True,
        'playliststart': 1,
        'playlistend': 1,
        'age_limit': 0,
        'quiet:': True,
        'extract_flat': 'in_playlist'
    }

    # check if the playlist is a valid and public by getting the information of a random video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        # extract info
        info = ydl.extract_info(clear_url, download=False)
        if info is None:
            # if info not extracted (non valid url)
            return False, 'Your Query does not contain a valid youtube playlist id'
        else:
            # if info extracted (valid url)
            return clear_url, None


if __name__ == '__main__':
    # DEBUG
    print('WORK')
    print(check_query('https://www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    print(check_query('ps://www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    print(check_query('//www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    print(check_query('www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    print(check_query('youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    print(check_query('https://www.youtube.com/watch?v=AEtbFm_CjE0&list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    print(check_query('https://www.youtube.com/watch?v=AEtbFm_CjE0&list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX&index=1'))
    print(check_query('https://www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX&watch?v=AEtbFm_CjE0'))
    print(check_query('https://www.youtube.com/playlist?list=PLNyOBdEynvBp1E\t03WBh33-P\rhBG9 WSQ-uX\n'))

    print('\nERROR')
    print(check_query(''))  # empty string
    print(check_query('dfg\rhuyt|df-.\n\t'))  # random string
    print(check_query('https://www.youtube.com/watch?v=jNQXAC9IVRw'))  # youtube video link
    print(check_query('https://www.youtube.com/playlist?list='))  # empty playlist id
    print(check_query('https://www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uC'))  # invalid playlist id
