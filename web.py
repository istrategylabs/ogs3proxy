from decouple import config
from flask import Flask, redirect, render_template, request

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

S3_BUCKET = config('S3_BUCKET')
REDIRECT_URL = config('REDIRECT_URL')
OG_TITLE = config('OG_TITLE')
OG_DESCRIPTION = config('OG_DESCRIPTION')

S3_ROOT = 'https://s3.amazonaws.com/'

app = Flask(__name__)


def is_facebook(ua):
    return ua.startswith('facebookexternalhit') or ua == 'Facebot'


@app.route("/<path:path>", methods=['GET'])
def opengraph(path):

    ua = request.headers.get('User-Agent')

    if is_facebook(ua) or 'fb' in request.args:

        context = {
            'og_title': OG_TITLE,
            'og_description': OG_DESCRIPTION,
            'og_image': urljoin(S3_ROOT, '{}/{}'.format(S3_BUCKET, path)),
            'og_url': '/{}'.format(path),
        }
        return render_template('opengraph.html', **context)

    else:

        return redirect(REDIRECT_URL)


if __name__ == "__main__":
    DEBUG = config('DEBUG', default=False, cast=bool)
    PORT = config('PORT', default=8000, cast=int)
    app.run(debug=DEBUG, port=PORT)
