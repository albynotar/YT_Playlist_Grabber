from urllib.parse import urlparse
import yt_dlp
import re

"""
Function that checks and cleans the query inserted as input
"""


def check_query(query):
    if query == '':
        return False, 'Your Query is empty'
    # remove any special character from query
    url = re.sub(r'\s+', '', query)
    # analyze the query using urlparse
    o = urlparse(url)
    # DEBUG
    #print(url)
    #print(o)
    # if the link does not contain youtube return False
    if not o.netloc == 'www.youtube.com' and 'youtube.com' not in o.path:
        return False, 'Your Query is not a youtube link'
    # if the link does not contain a playlist query return False
    elif 'list=' not in o.query:
        return False, 'Your Query is not a playlist url'
    # if the link does not contain a playlist code return False
    playlist_id = o.query
    playlist_id.replace('list=','')
    clear_query = 'https://www.youtube.com/playlist?' + str(playlist_id)
    print(clear_query)
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
        info = ydl.extract_info(clear_query, download=False)
        if info is None:
            # if info not extracted (non valid url)
            return False, 'Your Query is not a valid playlist url'
        else:
            # if info extracted (valid url)
            return clear_query, None


if __name__ == '__main__':
    # DEBUG
    # work
    print(check_query(''))
    print(check_query('https://www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    print(check_query('www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    print(check_query('youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    print(check_query('https://www.youtube.com/watch?v=AEtbFm_CjE0&list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX&index=1'))
    print(check_query('https://www.youtube.com/watch?v=AEtbFm_CjE0&list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'))
    # dont work
    print(check_query('https://www.youtube.com/watch?v=jNQXAC9IVRw'))
    print(check_query('https://www.youtube.com/playlist?list=PLNyO\n\t\rBdEyngbhgFRGVTGC DRCWTQ\n\t\r'))
    print(check_query('https://www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uC'))
