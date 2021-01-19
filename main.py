# app.py
from flask import Flask, request, Response, jsonify
from io import BytesIO
from werkzeug import FileWrapper
import simplekml
app = Flask(__name__)


@app.route('/convert/', methods=['POST'])
def convert():
    param = request.form.get('name')
    kml = simplekml.Kml()
    pnt = kml.newpoint(name="A Point")
    print(kml.kml())
    # Use BytesIO instead of StringIO here.
    b = BytesIO(kml.kml().encode('UTF-8'))
    w = FileWrapper(b)
    return Response(w, mimetype="application/vnd.google-earth.kml+xml",
                    headers={"Content disposition": "attachment; filename=converted.kml"}, direct_passthrough=True)


@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return app.send_static_file('index.html')


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
