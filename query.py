import yt_dlp
import re

"""
Function that checks and cleans a query inserted as input.
The query must contain a valid yt-playlist ID to pass the validation.
"""


def check_query(query):
    # remove any special character from query
    url = re.sub(r'\s+', '', query)

    # adjusted query
    playlist_id = re.findall(r'[0-9A-Za-z_-]{24,34}', url)

    if not playlist_id:
        return False, 'Your Query does not contain a youtube playlist id'
    else:
        clear_url = 'https://www.youtube.com/playlist?list=' + str(playlist_id[0])

    # settings for logger to not print anything in command line
    class Logger:

        def debug(self, msg):
            pass

        def info(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            pass

    # options to extract info
    ydl_opts = {
        'logger': Logger(),
        'forcejson': True,
        'ignoreerrors': False,
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
        try:
            info = ydl.extract_info(clear_url, download=False)
        except (yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError):
            return False, 'Your Query does not contain a valid youtube playlist id'

        if info is None:
            # if info not extracted (non valid url)
            return False, 'Your Query does not contain a valid youtube playlist id'
        else:
            # if info extracted (valid url)
            return clear_url, None


if __name__ == '__main__':
    # DEBUG
    with open('query_tests.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            print(check_query(line))
