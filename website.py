import youtube_dl
from flask import Flask, render_template, request, send_file

from extraction import processing

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/process', methods=['POST'])
def result():
    if request.method == 'POST':
        playlist_url = request.form['Playlist_URL']
        ydl_opts = {
            'ignoreerrors': True,
            'skip_download': True,
            'playlistrandom': True,
            'playliststart': 1,
            'playlistend': 1,
            'age_limit': 0,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info = ydl.extract_info(playlist_url, download=False)
            if info is None:
                return render_template('error.html')
            else:
                r = processing(playlist_url,
                               ['playlist_index', 'id', 'title', 'uploader', 'upload_date', 'view_count', 'like_count',
                                'dislike_count', 'average_rating', 'duration', 'age_limit', 'categories', 'webpage_url',
                                'alt_title', 'uploader_id', 'uploader_url', 'channel_id', 'channel_url', 'tags',
                                'thumbnails', 'description'])

                return render_template('process.html',
                                       playlist_table=r[0].to_html(classes='table is-striped is-fullwidth is-hoverable',
                                                                   index=False, header="true"),
                                       video_table=r[1].to_html(classes='table is-striped is-fullwidth is-hoverable',
                                                                index=False, header="true"))


@app.route('/download', methods=['POST'])
def download():
    path = request.form['Download']
    return send_file(path, as_attachment=True)


@app.route('/error')
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
