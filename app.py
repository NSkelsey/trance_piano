#written by nick
from flask import Flask, abort
import json
from urlparse import urlparse

app = Flask(__name__)

with open('./mikeSite.txt', 'r') as f:
    raw = f.read()
    url_dict = json.loads(raw)

def normalize_path(path):
    if path == '':
        path = '/'
    if not path.startswith('/'):
        path = '/' + path
    if not path.endswith('/'):
        path = path + '/'
    return path

def build_from_scrape(url_dict):
    _copy_d = dict()
    for key, value in url_dict.iteritems():
        key = normalize_path(key)
        _copy_d[key] = [normalize_path(v) for v in value]
    url_dict = _copy_d
    return url_dict

# returns tuple of (if internal link, path) <-- (false, none) if no
def format_internal(url, parsed_site):
    url = urlparse(url)
    if url.scheme != 'http':
        return (False, None)
    if (url.netloc == parsed_site.netloc 
      or url.netloc == '.'.join(parsed_site.netloc.split('.')[-2:])):
        return (True, url.path)
    else: return (False, None)

def build_from_referrers(url_dict, root_url):
    parsed = urlparse(root_url)
    _copy_d = dict()
    for key in url_dict.keys():
        if key not in _copy_d: 
            key_path = normalize_path(key)
            _copy_d[key_path] = set()
    for key, values in url_dict.iteritems():
        key = normalize_path(key)
        for refer in values:
            internal, path = format_internal(refer, parsed)
            if internal:
                path = normalize_path(path)
                if path in _copy_d:
                    _copy_d[key].add(path)
    return _copy_d

url_dict = build_from_referrers(url_dict, "http://www.plagiarismtoday.com")

print url_dict

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


