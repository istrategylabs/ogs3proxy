import logging
import uuid
from decouple import config
from flask import Flask, redirect, render_template, request

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

S3_ROOT = 'https://s3.amazonaws.com/'
S3_BUCKET = config('S3_BUCKET')
REDIRECT_URL = config('REDIRECT_URL')
OG_TITLE = config('OG_TITLE')
OG_DESCRIPTION = config('OG_DESCRIPTION')
FB_APP_ID = config('FB_APP_ID')


# We kind of have to have a static folder, so generate some random
# one that should never match an actual S3 path.
# If it conflicts, restart the process until it doesn't.
app = Flask(__name__, static_folder=uuid.uuid4().hex)


logger = logging.getLogger('ogs3proxy')
logger.info('Using static folder: {}'.format(app.static_folder))


def is_facebook(ua):
    return ua.startswith('facebookexternalhit') or ua == 'Facebot'


@app.route("/", methods=['GET'])
def index():
    return redirect(REDIRECT_URL)


@app.route("/<path:path>", methods=['GET'])
def opengraph(path):

    ua = request.headers.get('User-Agent')

    if is_facebook(ua) or 'fb' in request.args:

        context = {
            'og': {
                'title': OG_TITLE,
                'description': OG_DESCRIPTION,
                'image': urljoin(S3_ROOT, '{}/{}'.format(S3_BUCKET, path)),
                'url': request.base_url,
            },
            'fb': {
                'app_id': FB_APP_ID,
            },
        }
        return render_template('opengraph.html', **context)

    else:

        return redirect(REDIRECT_URL)


if __name__ == "__main__":
    DEBUG = config('DEBUG', default=False, cast=bool)
    PORT = config('PORT', default=8000, cast=int)
    app.run(debug=DEBUG, port=PORT)
