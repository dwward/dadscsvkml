# app.py
from flask import Flask, request, Response, jsonify
from io import BytesIO, StringIO
from werkzeug import FileWrapper, secure_filename
import simplekml
import csv
app = Flask(__name__)


@app.route('/convert', methods=['POST'])
def convert():
    f = request.files['fileToUpload']
    csvf = StringIO(f.read().decode())
    people = csv.reader(csvf, delimiter=',')
    for row in people:
        print(row)
    # print(f.readline())
    kml = simplekml.Kml()
    pnt = kml.newpoint(name="A Point")
    """
    // county
    // townland
    // parish
    // lat
    // long
    // tl_tag
    // tl_name
    // tl_name_gaelic
    // alt_name_eng
    // alt_name_gaelic
    // barony
    // t_ie_url


		<Placemark>
			<name>Bartholomew Leydon 1858</name>
			<description>Griffith&apos;s Valuation, 1858, Ballyfarnon, Sligo</description>
			<LookAt>
				<longitude>-8.205360093710597</longitude>
				<latitude>54.07312273318456</latitude>
				<altitude>0</altitude>
				<heading>-0.0005324890063178158</heading>
				<tilt>9.536247145736597</tilt>
				<range>1107.088523831614</range>
				<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
			</LookAt>
			<styleUrl>#msn_placemark_circle01</styleUrl>
			<Point>
				<gx:drawOrder>1</gx:drawOrder>
				<coordinates>-8.205837825368928,54.07378468073625,0</coordinates>
			</Point>
		</Placemark>
    """

    print(kml.kml())
    # Use BytesIO instead of StringIO here.
    b = BytesIO(kml.kml().encode('UTF-8'))
    w = FileWrapper(b)
    return Response(w, mimetype="application/vnd.google-earth.kml+xml",
                    headers={"content-disposition": "attachment; filename=converted.kml"}, direct_passthrough=True)


@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return app.send_static_file('index.html')


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
