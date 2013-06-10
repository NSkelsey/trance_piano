import string
import random

from flask import Flask

app = Flask(__name__)

def generate_text(length = 1):
    random_char = "".join(random.sample(string.ascii_letters, length))
    return random_char

@app.route('/shoes/<randstr>')
def deeper(randstr):
    page_text = "<p>{0}</p><ul>{1}</ul>"
    p = generate_text(50)
    a = generate_links(randstr)
    html = page_text.format(p,a)
    return html

def generate_links(root=None):
    base = '<ul><a href="{0}{1}" >turtles!</a></ul>'
    a_str = str()
    for i in range(20):
        extra = generate_text(4)
        if len(root + extra) > 25:
                extra = extra[-20:]
                root = '/shoes/'
        a = base.format(root, extra)
        a_str += a
    return a_str

@app.route('/')
def home():
    html = "This is home <ul>{0}</ul>".format(generate_links('/shoes/'))
    return html

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)


