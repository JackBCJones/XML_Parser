from flask import Flask, request, jsonify, send_file, after_this_request
import xml.etree.ElementTree as ET
import json
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, allow_headers=['Content-Type'])


@app.route('/upload', methods=['POST'])
def upload_file():
    # print("Uploading file")
    file = request.files['file']
    tree = ET.parse(file)
    root = tree.getroot()

    events = []

    for game in root.findall('Game'):
        for event in game.findall('Event'):
            x = round(float(event.get('x')) * 1.15, 1)
            y = round(float(event.get('y')) * 0.74, 1)
            if x > 0.0 and y > 0.0:
                type_id = int(event.get('type_id'))
                team_id = int(event.get('team_id'))
                outcome = int(event.get('outcome'))
                period_id = int(event.get('period_id'))
                qualifiers = []
                names = []
                for qualifier in event:
                    qualifier_id = int(qualifier.get('qualifier_id'))
                    qualifiers.append(qualifier_id)
                events.append({'x': x, 'y': y, 'type_id': type_id, 'qualifiers': qualifiers, 'team_id': team_id, "outcome": outcome, "period_id": period_id, "names": names})

    # Save the events as a JSON file
    json_filename = f'{file.filename}_new.json'
    with open(json_filename, 'w') as jsonfile:
        json.dump(events, jsonfile)

    @after_this_request
    def delete_file(response):
        # Delete the file from the file directory
        os.remove(json_filename)
        return response

    # Return the JSON file for download
    return send_file(json_filename, as_attachment=True)




if __name__ == '__main__':
    app.run()
