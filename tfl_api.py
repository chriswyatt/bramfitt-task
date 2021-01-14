from urllib.parse import quote

import requests
from werkzeug.exceptions import abort

from serializers import create_prediction_pb


def get_arrival_predictions(naptan_id):
    url = f'https://api.tfl.gov.uk/StopPoint/{quote(naptan_id)}/arrivals'
    response = requests.get(url)

    if response.status_code != 200:
        abort(502)

    for prediction_dict in response.json():
        prediction = create_prediction_pb(prediction_dict)
        yield prediction
