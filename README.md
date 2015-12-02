# Open Graph S3 Proxy

Proxy requests for images on S3 to provide standard Open Graph tags.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

A request by the Facebook crawler to `http(s)://<domain>/<path>` will generate a unique page for the object stored at `https://s3.amazonaws.com/<bucket>/<path>`. This page contains Open Graph tags and basic page content.

All other user agents will be redirected to the specified redirect URL. To view the page that the Facebook crawler receives, add the `?fb` query string parameter to the end of the URL.

## Configuration

All configuration is done through environment variables.

| Variable | Description |
|----------|-------------|
| SECRET_KEY | A unique value used for signing |
| DEBUG | Debug mode, default `False` |
| FB_APP_ID | Facebook app ID |
| REDIRECT_URL | Redirect URL for non-Facebook requests |
| S3_BUCKET | The bucket containing the proxied S3 objects |
| OG_TITLE | Open Graph title |
| OG_DESCRIPTION | Open Graph description |


