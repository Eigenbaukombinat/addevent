import create_event
from flask import Flask, render_template, request, make_response
from datetime import datetime

app = Flask("calwebadd")
APPROOT = '/'


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)


def to_dict(args):
    outdict = {}
    for key, val in args.items():
        outdict[key] = val
    return outdict

# format used for parsing
FMT = '%d.%m.%Y %H:%M'

@app.route('/')
def index():
    return render_template(
        'index.html', 
        title='',
        start='',
        end='',
        desc='',
        errors=[],
        approot=APPROOT)


@app.route('/addevent', methods=['POST'])
def addevent():
    data = to_dict(request.form)
    title = data.get('title', '')
    start = data.get('start', '')
    end = data.get('end', '')
    public = data.get('public', '')
    desc = data.get('desc', '')

    # validation

    errors = []

    if len(title) < 5:
        errors.append('Der Titel ist zu kurz.')

    try:
        start_dt = datetime.strptime(start, FMT)
        end_dt = datetime.strptime(end, FMT)
    except ValueError:
        errors.append('Datumsformat passt nicht.')

    public_b = True if public == 'true' else False

    if not len(errors):
        # no errors, create the event!
        ev = create_event.add_event(
            title,
            start_dt,
            end_dt,
            desc,
            public_b)
        return render_template(
            'thx.html',
            approot=APPROOT,
            evdata=ev.data)
    else:
        return render_template(
            'index.html',
            errors=errors, 
            title=title,
            start=start,
            end=end,
            desc=desc,
            approot=APPROOT)
