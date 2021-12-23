from flask import Flask, render_template, request, send_file
from query import check_query
from extraction import processing

app = Flask(__name__)


# route of homepage
@app.route('/')
def home_page():
    return render_template('home_page.html')


# route after clicking the submit button
@app.route('/process', methods=['POST'])
def result():
    if request.method == 'POST':
        playlist_url = str(request.form['Playlist_URL']).strip()

        info_attributes = set()
        for key, value in request.form.items():
            if key != 'Playlist_URL':
                info_attributes.add(value)
        query_check, error_message = check_query(playlist_url)
        # setting to extract info_json from a random video of playlist
        if not query_check:
            return render_template('error.html', query='"'+playlist_url+'"', error_message=error_message)
        else:
            r = processing(str(query_check), info_attributes)
            # render process template with results as tables
            return render_template('process.html',
                                   playlist_table=r[0].to_html(classes='table is-narrow is-striped is-fullwidth is-hoverable',
                                                               index=False, header="true"),
                                   video_table=r[1].to_html(classes='table is-narrow is-striped is-fullwidth is-hoverable',
                                                            index=False, header="true"))


# route for downloading a data table as json
@app.route('/download', methods=['POST'])
def download():
    path = request.form['Download']
    return send_file(path, as_attachment=True)


# route for error page
@app.route('/error')
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
