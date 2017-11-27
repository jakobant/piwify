from flask import Flask, jsonify, Response
from flask import render_template
from flask import make_response
from flask import request
import piwify
import os

pi = piwify.Piwify("wlp3s0")


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

app = Flask(__name__)
@app.route('/wifi', methods=['GET'])
def show_wifi():
    data = request.json
    stuff = pi.get_wifi_list()
    return make_response(jsonify(stuff), 200)

@app.route('/reboot', methods=['GET'])
def reboot():
    pi.reboot()
    return make_response("Rebooting", 200)

@app.route('/set_wifi', methods=['POST', 'GET'])
def set_wifi():
    if request.method == 'GET' and request.args.get('sid') != None and request.args.get('key') != None:
        essid = request.args.get('sid')
        key =  request.args.get('key')
        print(essid, key)
        pi.add_wpa_config(essid, key)
        return make_response("Finished : Rebooting", 200)
    return make_response("Missig data", 200)


@app.route('/')
def index():
    return render_template("index.html",
                           title='Home')

@app.route('/static/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5678')

#sudo iwlist wlan0 scan | egrep "ESSID|Quality|Authentication|Channel|Address" > wifi.stuff