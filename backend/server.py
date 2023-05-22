from flask import Flask, request, jsonify, send_file, after_this_request
import xml.etree.ElementTree as ET
from flask.helpers import send_from_directory
import json
import os
import uuid
# from flask_cors import CORS, cross_origin
from functions import calculate_rarity, assign_names, assign_scores

app = Flask(__name__, static_folder='FANBLOCK/client/dist', static_url_path='')
# cors = CORS(app)


@app.route('/upload', methods=['POST'])
# @cross_origin()
def upload_file():
    # print("Uploading file")
    file = request.files['file']
    tree = ET.parse(file)
    root = tree.getroot()

    events = []

    x_multiplier = float(request.args.get('x_multiplier', '1.15'))
    y_multiplier = float(request.args.get('y_multiplier', '0.74'))

    for game in root.findall('Game'):
        for event in game.findall('Event'):
            unique_id = str(uuid.uuid4())
            x = round(float(event.get('x')) * x_multiplier, 1)
            y = round(float(event.get('y')) * y_multiplier, 1)
            type_id = int(event.get('type_id'))
            team_id = int(event.get('team_id'))
            outcome = int(event.get('outcome'))
            period_id = int(event.get('period_id'))
            qualifiers = []
            for qualifier in event:
                qualifier_id = int(qualifier.get('qualifier_id'))
                qualifiers.append(qualifier_id)
            events.append({'id': unique_id, 'x': x, 'y': y, 'type_id': type_id, 'qualifiers': qualifiers, 'team_id': team_id, "outcome": outcome, "period_id": period_id})

    events_with_rarity = calculate_rarity(events)
    events_with_names = assign_names(events_with_rarity)
    events_with_scores = assign_scores(events_with_names)

    # Save the events as a JSON file
    json_filename = f'{file.filename}_new.json'
    with open(json_filename, 'w') as jsonfile:
        json.dump(events_with_scores, jsonfile, indent=4)

    @after_this_request
    def delete_file(response):
        # Delete the file from the file directory
        os.remove(json_filename)
        return response

    # Return the JSON file for download
    return send_file(json_filename, as_attachment=True)

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
