import os

from typing import Tuple

import dill
import pandas as pd
import flask


app = flask.Flask(__name__)


# Load Boston house price prediction model
path = r'/usr/src/app/model'
with open(os.path.join(path, 'boston-model.dill'), 'rb') as file:
    model = dill.load(file)


# Load Boston dataset average values
features_avg = pd.read_csv(os.path.join(path, 'boston-features-avg.csv'), index_col=0)


# Call prediction, set average value for feature if it missing in input
def predict_price(features: dict) -> Tuple[dict, float]:
    features_vector = features_avg.copy()
    for key, value in features.items():
        try:
            features_vector[key][0] = float(value)
        except (KeyError, ValueError):
            pass

    return features_vector.to_dict('records')[0], model.predict(features_vector)[0]


@app.route('/')
def hello():
    return 'Hello!'


@app.route("/predict", methods=["POST"])
def predict():
    features, price = predict_price(flask.request.get_json())
    result = {'features': features, 'predict': price}
    return flask.jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
