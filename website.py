from flask import Flask, render_template, request, send_file, redirect
from query import check_query
from extraction import processing
from werkzeug.exceptions import HTTPException

"""
Webpage to ask and receive particular information about a yt playlist.
Information is obtained with yt-dlp and it is displayed on the webpage with pandas dataframes.
Webpage created with Flask.
"""

app = Flask(__name__)

# route of homepage
@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home_page.html')


# route after clicking the submit button
@app.route('/process', methods=['GET', 'POST'])
def result():

    if request.method == 'POST':
        # get playlist url from form
        # limit to first 150 characters
        playlist_url = str(request.form['Playlist_URL'][0:150]).strip()

        # get attributes to extract from form
        info_attributes = set()
        for key, value in request.form.items():
            if key != 'Playlist_URL':
                info_attributes.add(value)

        # query validation
        query_check, error_message = check_query(playlist_url)

        # if query check return False
        if not query_check:
            # reduce query length if too long > 50
            if len(playlist_url) > 50:
                playlist_url = playlist_url[:20] + ' [...] ' + playlist_url[-20:]
            return render_template('query_error.html', query=playlist_url, error_message=error_message)
        # if query check passed
        else:
            # extract info using extraction.py processing function
            r = processing(str(query_check), info_attributes)
            # render process template with results as tables
            return render_template('process.html',
                                   playlist_table=r[0].to_html(
                                       classes='table is-narrow is-striped is-fullwidth is-hoverable',
                                       index=False, header="true"),
                                   video_table=r[1].to_html(
                                       classes='table is-narrow is-striped is-fullwidth is-hoverable',
                                       index=False, header="true"))
    else:
        return redirect('/')


# route for downloading a data table as json
@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        path = request.form['Download']
        return send_file(path, as_attachment=True)
    else:
        return redirect('/')


# route for query error page
@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        return render_template('query_error.html')
    else:
        return redirect('/')


# route for handling errors
@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return render_template("error.html", code=str(e.code), description=str(e.description)), str(e.code)
    # handle non-HTTP exceptions only
    return render_template("error.html", code=500, description='generic error'), 500


if __name__ == '__main__':
    app.run()
    # DEBUG
    # app.run(debug=True)
