import hashlib

# djng configures django, so it always has to come first.
import djng
from django import http

import settings


def bounce(request, hash, url):
    """Redirect to ``url``, but only if it matches the ``hash``."""
    print url
    expected = hashlib.sha1(settings.secret + url)
    if expected.hexdigest() == hash:
        return http.HttpResponseRedirect(url)
    else:
        return djng.Response('redirecting to /dev/null')


def home(request):
    url = 'http://github.com/jbalogh/moonshoes'
    return djng.Response('This is <a href="%s">moonshoes</a>' % url)



# Give the bouncer a v1 namespace so it can expand later.
app = djng.ErrorWrapper(djng.Router(
    ('^$', home),
    (r'^v1/([^/]+)/(.*)$', bounce),
))


if __name__ == '__main__':
    assert hasattr(settings, 'secret'), "Put a secret key in settings.py"
    djng.serve(app, '0.0.0.0', 8000)
