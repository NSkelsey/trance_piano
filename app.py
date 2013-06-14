from flask import Flask, abort
import json

app = Flask(__name__)

with open('site.json', 'r') as f:
    raw = f.read()
    url_dict = json.loads(raw)

def normalize_url(path):
    if path == '':
        path = '/'
    if not path.startswith('/'):
        path = '/' + path
    if not path.endswith('/'):
        path = path + '/'
    return path

_copy_d = dict()
for key, value in url_dict.iteritems():
    key = normalize_url(key)
    _copy_d[key] = [normalize_url(v) for v in value]
url_dict = _copy_d

print "These paths will all generate a valid response:\n", url_dict.keys()

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def all_paths(path):
    if path is '' or not path.startswith('/'):
        path = '/' + path
    if (path in url_dict or
       (not path.endswith('/') and path + '/' in url_dict)):
        hrefs = url_dict[path]
        page = "<html><head></head><body><ul>\n"
        for href in hrefs:
            link = "<li><a href={0}>{0}</a></li>\n".format(href)
            page += link
        page += "</ul></body></html>"
        return page
    else:
        abort(404)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


