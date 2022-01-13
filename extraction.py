import yt_dlp
import json
import pandas as pd

"""
Request a valid yt playlist url and a set of attributes to download the function.
The function returns two .json files (playlist_info.json and video_info.json) with the 
playlist info and its videos info requested and 
two pandas dataframes for displaying the information to the webpage
"""


def processing(u, filter_keys):
    # settings for logger to not print anything in command line
    class MyLogger:

        def debug(self, msg):
            # For compatability with youtube-dl, both debug and info are passed into debug
            # You can distinguish them by the prefix '[debug] '
            if msg.startswith('[debug] '):
                pass
            else:
                self.info(msg)

        def info(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            pass

    # download settings
    ydl_opts = {
        'logger': MyLogger(),
        'quiet': True,
        'forcejson': True,
        'ignoreerrors': True,
        'skip_download': True,
        'playlistreverse': True,
        'age_limit': 0,
        'clean_infojson': False,
        'check_formats': False
    }

    # fast download if specific arguments are selected
    fast_keys = {'id', 'title', 'duration', 'uploader', 'webpage_url'}

    if filter_keys.issubset(fast_keys):
        ydl_opts['extract_flat'] = 'in_playlist'
        if 'webpage_url' in filter_keys:
            filter_keys.remove('webpage_url')
            filter_keys.add('url')

    # process with YoutubeDL function from YoutubeDL.py
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # reset cache
        ydl.cache.remove()
        # extract information
        info = ydl.extract_info(u, download=False)

        # playlist info
        playlist_info = info.copy()
        playlist_info.pop("entries")

        # video info
        video_info = info['entries'].copy()

    # save json with playlist_information
    with open('playlist_info.json', 'w') as j_file:
        json.dump(playlist_info, j_file, indent=4)
    # create playlist table to be published on the webpage
    dt_playlist = pd.DataFrame({k: [v] for k, v in playlist_info.items()})
    dt_playlist.reset_index(inplace=True)

    # filter video info
    video_data = []
    for vid in video_info:
        try:
            video_data.append({k: j for (k, j) in vid.items() if k in filter_keys})
        # except removed/private/age-restricted videos
        except AttributeError:
            video_data.append({k: None for k in filter_keys})

    # replace None in playlist index of removed/private/age-restricted videos
    # with playlist index number by checking the video before it
    if 'playlist_index' in filter_keys:
        for i in range(len(video_data)):
            if video_data[i]['playlist_index'] is None:
                video_data[i]['playlist_index'] = video_data[i - 1]['playlist_index'] - 1

    # save json with video_information
    with open('video_info.json', 'w') as j_file:
        json.dump(video_data, j_file, indent=4)

    # create videos table to be published on the webpage
    dt_videos = pd.DataFrame.from_records(video_data)
    dt_videos.reset_index(inplace=True)

    # send to the website the tables (first 10 elements for videos table)
    return dt_playlist, dt_videos.head(10)


if __name__ == '__main__':
    # DEBUG
    link = 'https://www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'
    set_of_arguments = {'playlist_index', 'id', 'title', 'uploader', 'upload_date', 'view_count', 'like_count',
                        'average_rating', 'duration', 'age_limit', 'categories', 'webpage_url', 'alt_title',
                        'uploader_id', 'uploader_url', 'channel_id', 'channel_url', 'tags', 'thumbnails',
                        'description'}
    set_of_arguments1 = {'id', 'title', 'duration', 'uploader', 'webpage_url'}
    processing(link, set_of_arguments)
    processing(link, set_of_arguments1)
