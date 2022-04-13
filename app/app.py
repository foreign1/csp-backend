from random import random
import random
import math
import location_data
import json
import pickle
from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET', 'POST'])
def welcome():
    return "Hello World!"


@app.route("/predict/", methods=["POST"])
def predict():
    request_data = request.get_json()['body']
    pred_vars = []

    # verify age, fever, shortness-of-breath and chest pain in request
    if 'age' in request_data:
        pred_vars.append(1)
    else:
        pred_vars.append(0)
    if 'fever' in request_data:
        pred_vars.append(1)
    else:
        pred_vars.append(0)
    if 'shortness-of-breath' in request_data:
        pred_vars.append(1)
    else:
        pred_vars.append(0)
    if 'chest pain' in request_data:
        pred_vars.append(1)
    else:
        pred_vars.append(0)

    if len(request_data) == 0:
        return jsonify({
            "prediction": 0,
            "percentage": 0,
            "description": "LOW",
            "phone": [0],
            "address": "",
            "state": ""
        })

    return jsonify(pred(request_data))


def pred(data):
    percent = math.floor(random.random() * 100)
    prediction = 0
    description = ""
    if (percent < 33):
        prediction = 1
        description = "LOW"
    elif (percent < 66):
        prediction = 2
        description = "MEDIUM"
    else:
        prediction = 3
        description = "HIGH"

    # prepare response data
    state = data['state'].lower()
    location_info = location_data.location_data[state]
    address = location_info['location']
    phone = location_info['phone']
    recommendations = ['Wash your hands often',
                       'See a virtual councellor',
                       'Maintain healthy and hygenic diet',
                       'Ensure normal respiratory rate is achievable',
                       'Social distancing',
                       'Use of face mask',
                       'Vaccination',
                       'Regular cleaning and disinfection',
                       'Daily logging of patients’ vitals',
                       'Diarying daily oxygen saturation levels, pulse rate, and body temperature',
                       'Self-isolation including staying at home; avoiding touching other people; staying isolated in a specific room away from other people; use of a separate bathroom or washroom if possible; avoidance of sharing personal household items with other people or pets where possible and if not possible, these items should be cleaned with soap and warm water',
                       'Avoid handling pets',
                       'Wearing a mask covering the nose and mouth when around other people',
                       'Cleaning and disinfection are recommended on a daily basis including all high-touch surfaces',
                       'In order to reduce the spread of the SARS-CoV-2 virus, hand and finger sanitation should be practiced often with either soap and warm water or hand sanitizer',
                       'Counselling',
                       'Maintain healthy and hygienic diet'
                       ]

    return(
        {
            "prediction": prediction,
            "percentage": percent,
            "description": description,
            "address": address,
            "phone": phone,
            "recommendations": recommendations
        }
    )
