`moonshoes`_ is a redirection service that will make your urls a lot longer.
Why another redirector?

1. We can't link directly to any user-submitted urls on sites like
http://addons.mozilla.org because we don't want people installing malicious
Firefox add-ons from bad links on our site.

2. We don't want to use a shortener like http://bit.ly since that obscures the
final destination of the url.

3. We want to add a hash for security, so that attackers don't try to use the
mozilla redirector to give credibility to a malicious site.

moonshoes creates urls that look like
::

    example.com/moonshoes/<hash>/<the real url>

This is a link to http://mozilla.com for my moonshoes on localhost::

    localhost:8000/v1/56b9065481e3d4fe57669fbfef932381d004faca/http://mozilla.com


Usage
-----

A moonshoes link is created by taking the sha1 hash of your url and a secret
shared between your server and a moonshoes server.
::

    >>> import hashlib
    >>> secret = 'omgsecret'
    >>> url = 'http://mozilla.com'
    >>> hash = hashlib.sha1(secret + url).hexdigest()
    >>> link = 'example.com/moonshoes/%s/%s' % (hash, url)

If you're creating links that are going to be viewed in a browser, make sure you
url-encode the url *after* you create the hash.  The link needs to be encoded to
preserve any query or fragment pieces.  Otherwise, the query parameters will be
taken as parameters to moonshoes and the fragment will be completely dropped.

The right way to create a link::

    >>> import urllib2, hashlib
    >>> secret = 'omgsecret'
    >>> url = 'http://mozilla.com'
    >>> hash = hashlib.sha1(secret + url).hexdigest()
    >>> print '<a href="example.com/moonshoes/%s/%s>Redirect</a>' % (hash, urllib2.quote(url))
    <a href="example.com/moonshoes/56b9065481e3d4fe57669fbfef932381d004faca/http%3A//mozilla.com>Redirect</a>

Installation
------------

moonshoes is only available from source at the moment.  It can be retrieved from
its home on github with::

    git clone git://github.com/jbalogh/moonshoes.git

Now you should set up your virtual environment using either `virtualenv`_ or
`virtualenvwrapper`_.  I like virtualenvwrapper, so I say
::

    mkvirtualenv --python=/usr/local/bin/python2.6 --no-site-packages moonshoes

and then install `pip`_ in the virtual environment with::

    easy_install pip

Now you can download the requirements for moonshoes::

    pip install -r  moonshoes/requirements.txt


Setup
-----

moonshoes expects you to make a python file called settings.py and hide your
secret key in there.  It's in a separate file so it stays out of revision
control.

settings.py::

    secret = 'omgsecret'

Once you have a secret key, moonshoes is ready to go!  Run it like this::

    python moonshoes.py

This will start a toy server running on ``localhost:8000``.  If you used
``'omgsecret'`` as your secret (for shame!),
http://localhost:8000/v1/11724597ebf0e0415f92df56da7f2ca3f56f728f/http://github.com/jbalogh/moonshoes
should redirect you to the moonshoes homepage.


Production
----------

Let me get back to you on that one.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _moonshoes: http://github.com/jbalogh/moonshoes
.. _pip: http://pypi.python.org/pypi/pip
