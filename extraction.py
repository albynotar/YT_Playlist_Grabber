import json
import pandas as pd
import youtube_dl

def processing(u, filter_keys):
    ydl_opts = {
        'ignoreerrors': True,
        'skip_download': True,
        'playlistreverse': True,
        'sleep_interval': 5,
        'max_sleep_interval': 10,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()

        info = ydl.extract_info(u, download=False)
        playlist_info = {k: info[k] for k in info.keys() if k != 'entries'}
        with open('playlist_information.json', 'w', encoding='utf-8') as j_file:
            json.dump(playlist_info, j_file)
        dt_playlist = pd.DataFrame({k: [v] for k, v in playlist_info.items()})
        video_info = info['entries']
        with open('video_information.json', 'w', encoding='utf-8') as j_file:
            json.dump(video_info, j_file)
        with open('video_information.json', 'r', encoding='utf-8') as f:
            videos = json.load(f)
        data = []
        for vid in videos:
            try:
                data.append({k: j for (k, j) in vid.items() if k in filter_keys})
            except AttributeError:
                data.append({k: None for k in filter_keys})
        for i in data:
            if i['playlist_index'] is None:
                i['playlist_index'] = data.index(i) + 1
            print(i)
        with open('video_information.json', 'w', encoding='utf-8') as j_file:
            json.dump(data, j_file)
        dt_videos = pd.read_json('video_information.json', encoding='utf-8')

        filter_keys.remove('tags')
        filter_keys.remove('thumbnails')
        filter_keys.remove('description')

        dt_videos = dt_videos[filter_keys]
        return dt_playlist, dt_videos


if __name__ == '__main__':
    link = 'https://www.youtube.com/playlist?list=PLNyOBdEynvBp1E03WBh33-PhBG9WSQ-uX'
    print(processing('kjhgf',
                     ['playlist_index', 'id', 'title', 'uploader', 'upload_date', 'view_count', 'like_count',
                      'dislike_count', 'average_rating', 'duration', 'age_limit', 'categories', 'webpage_url',
                      'alt_title', 'uploader_id', 'uploader_url', 'channel_id', 'channel_url', 'tags', 'thumbnails',
                      'description']))
