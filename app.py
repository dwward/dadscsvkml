# app.py
from flask import Flask, request, Response, jsonify
from io import BytesIO, StringIO
from werkzeug import FileWrapper, secure_filename
import simplekml
import csv
import pandas as pd


def load_townland_data():
    filename = 'townlands-no-geom-0907202-0810.csv'
    # Townland fields of interest
    # OSM Dict: OSM_ID(0), NAME_TAG(1), NAME_ENG(3), PARISH(13), COUNTY(10)
    # datatype = {'ATTRIBUTIO': string}
    # OSM_ID, NAME_TAG, NAME_GA, NAME_EN, ALT_NAME, ALT_NAME_G, OSM_USER, OSM_TIMEST, ATTRIBUTIO, LOGAINM_RE, CO_NAME, CO_OSM_ID, CO_LOGAINM, CP_NAME, CP_OSM_ID, CP_LOGAINM, ED_NAME, ED_OSM_ID, ED_LOGAINM, BAR_NAME, BAR_OSM_ID, BAR_LOGAIN, T_IE_URL, AREA, LATITUDE, LONGITUDE, EPOCH_TSTM
    # int, string, string, string, string, string, string, datetime, string, int, string, float

    pd.set_option('display.max_columns', None)
    towndata = pd.read_csv(filename, dtype={8: 'string', 9: 'string'})
    return towndata


app = Flask(__name__)
app.townland = load_townland_data()


@app.route('/convert', methods=['POST'])
def convert():
    # Parse townlands data
    # f2 = request.files['file2']
    # f2 = StringIO(f2.read().decode())
    # f2_csv = csv.reader(f2, delimiter=',')
    # fields = next(f2_csv)
    # print(fields)

    # Parse file1 upload
    f1 = request.files['file1']
    f1 = StringIO(f1.read().decode())
    f1_csv = csv.reader(f1, delimiter=',')
    fields = next(f1_csv)

    for row in f1_csv:
        townland = row[2]
        parish = row[3]
        county = row[4]
        first_name = row[1]
        last_name = row[0]

        df = app.townland
        # loc = df[(df["CO_NAME"] == county) & (df["CP_NAME"] == parish)]
        loc = df[((df["NAME_TAG"] == townland) | (df["NAME_EN"] == townland))
                 & (df["CP_NAME"] == parish)
                 & (df["CO_NAME"] == county)]
        if loc.empty:
            print(first_name + ' ' + last_name + ' (' + county + ', ' + parish + ", " + townland + ')')

    kml = simplekml.Kml()
    pnt = kml.newpoint(name="A Point")  # f1-2 f1-1 f1-7
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
